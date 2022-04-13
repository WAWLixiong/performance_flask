import pymysql
from dbutils.pooled_db import PooledDB


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

    def __init__(self):
        self.pool = PooledDB(**self.config)

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def __exit__(self, type, value, trace):
        self.cursor.close()


if __name__ == '__main__':
    pool = MysqlPool()

    with pool as (conn, cursor):
        cursor.execute('select count(*) from t')
        print(cursor.fetchall())
