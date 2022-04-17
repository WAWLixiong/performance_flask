import pymysql
from dbutils.pooled_db import PooledDB
from threading import get_ident


class MysqlPool:
    config = {
        'creator': pymysql,
        'host': '192.168.9.128',
        'port': 3306,
        'user': 'root',
        'password': 'sqfh512.~',
        'db': 'orm',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    _cursor_cache = {}
    _conn_cache = {}

    def __init__(self):
        self.pool = PooledDB(**self.config)

    def __enter__(self):
        id_ = get_ident()
        conn = self.pool.connection()
        cursor = conn.cursor()
        self._cursor_cache[id_] = cursor
        self._conn_cache[id_] = conn
        return conn, cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        id_ = get_ident()
        self._cursor_cache[id_].close()
        self._conn_cache[id_].close()


if __name__ == '__main__':
    pool = MysqlPool()

    with pool as (conn, cursor):
        cursor.execute('select count(*) from t')
        print(cursor.fetchall())
