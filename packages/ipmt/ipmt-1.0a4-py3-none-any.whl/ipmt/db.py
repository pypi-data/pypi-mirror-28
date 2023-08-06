# -*- coding: utf-8 -*-
import logging
import psycopg2
from ipmt.error import DbError
from ipmt.misc import parse_dsn

READ_UNCOMMITTED = 'READ UNCOMMITTED'
READ_COMMITTED = 'READ COMMITTED'
REPEATABLE_READ = 'REPEATABLE READ'
SERIALIZABLE = 'SERIALIZABLE'

REL_TABLE = 'r'
REL_INDEX = 'i'
REL_SEQUENCE = 'S'
REL_VIEW = 'v'
REL_MATERIALIZED_VIEW = 'm'
REL_COMPOSITE_TYPE = 'c'
REL_TOAST_TABLE = 't'
REL_FOREIGN_TABLE = 'f'

VERSION_SCHEMA = 'public'

VERSION_TABLE = 'ipmt_version'

OPS_SCHEMA = 'public'

OPS_TABLE = 'ipmt_ops'

SQL_OPS_TABLE_EXISTS = """\
SELECT EXISTS (
    SELECT 1
    FROM   pg_catalog.pg_class c
    JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE  n.nspname = '%s'
    AND    c.relname = '%s'
    AND    c.relkind = 'r'
)
""" % (OPS_SCHEMA, OPS_TABLE)

SQL_VERSION_TABLE_EXISTS = """\
SELECT EXISTS (
    SELECT 1
    FROM   pg_catalog.pg_class c
    JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE  n.nspname = '%s'
    AND    c.relname = '%s'
    AND    c.relkind = 'r'
)
""" % (VERSION_SCHEMA, VERSION_TABLE)

SQL_OPS_CREATE = """\
CREATE TABLE %s.%s(
    id serial NOT NULL PRIMARY KEY,
    op text NOT NULL,
    old_version text,
    new_version text,
    stamp timestamptz NOT NULL DEFAULT NOW()
)
""" % (OPS_SCHEMA, OPS_TABLE)

SQL_VERSION_CREATE = """\
CREATE TABLE %s.%s(
    version text NOT NULL,
    history text[] NOT NULL
);
CREATE UNIQUE INDEX ON %s.%s((version IS NOT NULL));
""" % (VERSION_SCHEMA, VERSION_TABLE, VERSION_SCHEMA, VERSION_TABLE)

SQL_VERSION_CURRENT = """\
SELECT version FROM %s.%s
""" % (VERSION_SCHEMA, VERSION_TABLE)

SQL_VERSION_SET = """\
WITH del AS (DELETE FROM {}.{} RETURNING history)
INSERT INTO {}.{}(version, history)
SELECT %(version)s,
       ARRAY(SELECT UNNEST(del.history) FROM del) || ARRAY[]::text[]
""".format(VERSION_SCHEMA, VERSION_TABLE, VERSION_SCHEMA, VERSION_TABLE)

SQL_VERSION_UP = """\
WITH del AS (DELETE FROM {}.{} RETURNING history)
INSERT INTO {}.{}(version, history)
SELECT %(version)s,
       ARRAY(SELECT UNNEST(del.history) FROM del) || ARRAY[%(version)s]
""".format(VERSION_SCHEMA, VERSION_TABLE, VERSION_SCHEMA, VERSION_TABLE)

SQL_VERSION_DOWN = """\
WITH del AS (DELETE FROM {}.{} RETURNING history)
INSERT INTO {}.{}(version, history)
SELECT %(version)s,
       ARRAY(SELECT UNNEST(history[1:array_upper(history, 1) - 1]) FROM del)
WHERE %(version)s IS NOT NULL
""".format(VERSION_SCHEMA, VERSION_TABLE, VERSION_SCHEMA, VERSION_TABLE)

SQL_OPS_INSERT = """\
INSERT INTO {}.{}(op, old_version, new_version)
VALUES(%(op)s, %(old_version)s, %(new_version)s)
""".format(OPS_SCHEMA, OPS_TABLE)

SQL_HISTORY = """\
SELECT UNNEST(history) FROM {}.{}
""".format(VERSION_SCHEMA, VERSION_TABLE)

SQL_DB_SCHEMAS = """\
SELECT format('DROP SCHEMA IF EXISTS %I CASCADE;', nspname)
FROM pg_namespace
WHERE nspname NOT LIKE 'pg%'
      AND nspname <> 'public'
      AND nspname <> 'information_schema';
"""

SQL_SERCH_OBJECTS = """\
SELECT
        format('%%I.%%I', nspname, relname)
FROM
        pg_class,
        pg_namespace
WHERE
        relnamespace = pg_namespace.oid
        AND
        format('%%I.%%I', nspname, relname) ~ %(rel_pattern)s
        AND
        relkind = ANY(%(rel_kind)s::text[])
"""


class Database(object):
    def __init__(self, dsn):
        self._in_transaction = False
        self._isolation_level = None
        self.buffer = []
        self.dry_run = False
        host, port, user, pwd, dbname = parse_dsn(dsn)
        self.conn = psycopg2.connect(database=dbname, user=user, password=pwd,
                                     host=host, port=port)
        self.conn.set_session(autocommit=True)
        self.cursor = self.conn.cursor()
        self._initialized = False

    @property
    def in_transaction(self):
        return self._in_transaction

    @property
    def isolation_level(self):
        return self._isolation_level

    @property
    def current(self):
        return self._query_scalar_unlogged(SQL_VERSION_CURRENT)

    @current.setter
    def current(self, version):
        self._execute_unlogged(SQL_VERSION_SET, {"version": version})

    @property
    def history(self):
        return self._query_column_unlogged(SQL_HISTORY)

    @property
    def schemas(self):
        return self._query_column_unlogged(SQL_DB_SCHEMAS)

    def search_objects(self, name_pattern, object_kinds):
        """
        Search database objects by regex pattern

        Example:
        # searching all tables which name starts with "tbl_" in public schema
        objs = search_objects('^public.tbl_.*', [REL_TABLE, ])
        print(objs)
        > ["public.tbl_1", "public.tbl_2"]

        :param name_pattern: regex pattern including schema name
        :type: str
        :param object_kinds: list of objects
        :type: list
        :return: array of objects
        :rtype: list
        """
        if object_kinds is not None:
            object_kinds_param = "{%s}" % (",".join(object_kinds),)
        else:
            object_kinds_param = "{%s}" % (",".join((REL_TABLE, REL_INDEX,
                                                     REL_SEQUENCE, REL_VIEW,
                                                     REL_MATERIALIZED_VIEW,
                                                     REL_COMPOSITE_TYPE,
                                                     REL_TOAST_TABLE,
                                                     REL_FOREIGN_TABLE)),)
        params = {
            "rel_pattern": name_pattern,
            "rel_kind": object_kinds_param
        }
        return self.query_column(SQL_SERCH_OBJECTS, params)

    def execute(self, sql, params=None):
        if self.dry_run:
            self.buffer.append(sql)
        self._execute_unlogged(sql, params)

    def _execute_unlogged(self, sql, params=None):
        self._init_db()
        if not self.dry_run:
            self.cursor.execute(sql, params)

    def query_scalar(self, sql, params=None):
        if self.dry_run:
            self.buffer.append(sql)
        return self._query_scalar_unlogged(sql, params)

    def _query_scalar_unlogged(self, sql, params=None):
        self._execute_unlogged(sql, params)
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def query_all(self, sql, params=None):
        if self.dry_run:
            self.buffer.append(sql)
        return self._query_all_unlogged(sql, params)

    def _query_all_unlogged(self, sql, params=None):
        self._execute_unlogged(sql, params)
        return self.cursor.fetchall()

    def query_column(self, sql, params=None):
        if self.dry_run:
            self.buffer.append(sql)
        return self._query_column_unlogged(sql, params)

    def _query_column_unlogged(self, sql, params=None):
        self._execute_unlogged(sql, params)
        return [row[0] for row in self.cursor.fetchall()]

    def _init_db(self):
        if self._initialized:
            return
        self._initialized = True
        if not self._query_scalar_unlogged(SQL_OPS_TABLE_EXISTS):
            logging.debug("Creating table %s.%s" % (OPS_SCHEMA, OPS_TABLE))
            self._execute_unlogged(SQL_OPS_CREATE)
        if not self._query_scalar_unlogged(SQL_VERSION_TABLE_EXISTS):
            logging.debug("Creating table %s.%s" % (VERSION_SCHEMA,
                                                    VERSION_TABLE))
            self._execute_unlogged(SQL_VERSION_CREATE)

    def ops_add(self, op, old_version, new_version):
        if op not in ('up', 'down'):
            raise DbError('Invalid operation %s' % op)
        self._execute_unlogged(SQL_OPS_INSERT,
                               {"op": op, "old_version": old_version,
                                "new_version": new_version})
        if op == 'up':
            self._execute_unlogged(SQL_VERSION_UP, {"version": new_version})
        elif op == 'down':
            self._execute_unlogged(SQL_VERSION_DOWN, {"version": new_version})


def transactional(isolation_level=None):
    def decorator(fn, *args, **kwargs):
        def wrapper(*args, **kwargs):
            if len(args) > 0:
                db = args[0]
            elif 'db' in kwargs:
                db = kwargs['db']
            else:
                raise Exception()
            if db.in_transaction:
                return fn(*args, **kwargs)
            else:
                with Transaction(db):
                    return fn(*args, **kwargs)

        wrapper.__transactional__ = (isolation_level or
                                     READ_COMMITTED)
        return wrapper

    return decorator


class Transaction(object):

    def __init__(self, db, isolation_level=None):
        self.db = db
        self.isolation_level = isolation_level or READ_COMMITTED

    def begin(self):
        if self.db._in_transaction:
            raise DbError('There is already a transaction in progress')
        self.db.execute("BEGIN ISOLATION LEVEL %s;" % self.isolation_level)
        self.db._in_transaction = True
        self.db._isolation_level = self.isolation_level

    def commit(self):
        if not self.db._in_transaction:
            raise DbError('There is no transaction in progress')
        self.db.execute("COMMIT;")
        self.db._in_transaction = False
        self.db._isolation_level = None

    def rollback(self):
        if not self.db._in_transaction:
            raise DbError('There is no transaction in progress')
        self.db.execute("ROLLBACK;")
        self.db._in_transaction = False
        self.db._isolation_level = None

    def __enter__(self):
        self.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
