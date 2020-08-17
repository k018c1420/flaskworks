from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as db

db_param = {
    'user' : 'mysql',
    'host' : 'localhost',
    'password' : '',
    'database' : 'itemdb'
}

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = './static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    conn = db.connect(**db_param)       #   dbと接続
    cur = conn.cursor()                 #   操作用カーソル取得
    stmt = 'SELECT * FROM list'         #   クエリの設定
    cur.execute(stmt)                   #   クエリ実行
    rows = cur.fetchall()               #   実行結果を取得
    cur.close()                         #   カーソル閉じる
    conn.close()                        #   db接続解除
    return render_template('index.html', list=rows)


if __name__ == '__main__' :
    app.debug = True
    app.run()
