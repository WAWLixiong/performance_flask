from flask import Flask
from flask import jsonify
from utils.db_utils import MysqlPool

app = Flask(__name__)

db_pool = MysqlPool()

get_data_sql = "select * from t where id = 100001"
update_sql = "update t set count = count - 1 where id = 100001 and count - 1 >= 0"


@app.route('/info', methods=['post'])
def hello_world():
    """
    为什么 concurrent environment will raise Pymysql Cursor closed
    因为：db_pool 是全局对象, 并发时 self.conn, self.cursor会时常更新
    线程结束的时候什么对象的__del__被调用了？
    1.SteadyDBCursor
        1. cursor关闭
    2.PooledDedicatedDBConnection
        1. SteadyDBConnection(tough对象) 保存在 PooledDB 的 _idle_cache 中
    参考： 1. https://blog.csdn.net/gashero/article/details/1577187#id8
          2. 官网文档
    """
    # fixme: concurrent environment will raise Pymysql Cursor closed
    # done: 参考文档及源码说明 https://blog.csdn.net/gashero/article/details/1577187#id8
    # with db_pool as (conn, cursor):
    #     cursor.execute(get_data_sql)
    #     data_list = cursor.fetchall()
    #     if not data_list:
    #         return jsonify({'msg': 'no lottery left'})
    #     affect_rows = cursor.execute(update_sql)
    #     cursor.fetchone()
    #     if not affect_rows:
    #         conn.commit()
    #         return jsonify({'msg': 'lottery json no left'})
    #     conn.commit()
    # return jsonify(data_list[0])

    with db_pool as (conn, cursor):
        conn.begin()
        cursor.execute(get_data_sql)
        data_list = cursor.fetchall()
        if not data_list:
            return jsonify({'msg': 'no lottery left'})
        affect_rows = cursor.execute(update_sql)
        cursor.fetchone()
        if not affect_rows:
            conn.commit()
            return jsonify({'msg': 'lottery json no left'})
        conn.commit()
    return jsonify(data_list[0])


if __name__ == '__main__':
    app.run(host='192.168.9.128', port=9998, debug=True)
