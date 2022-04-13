from flask import Flask
from flask import jsonify
from utils.db_utils import MysqlPool

app = Flask(__name__)

db_pool = MysqlPool()

get_data_sql = "select * from t where id = 100001"
update_sql = "update t set count = count - 1 where id = 100001 and count - 1 >= 0"


@app.route('/info', methods=['post'])
def hello_world():
    with db_pool as (conn, cursor):
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
    app.run(debug=True)
