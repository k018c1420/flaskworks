from flask import Flask, render_template
import mysql.connector as db

db_param = {
    'user' : 'mysql',
    'host' : 'localhost',
    'password' : '',
    'database' : 'db1'
}

app = Flask(__name__)

@app.route('/')
def index():
    conn = db.connect(**db_param)   #   dbと接続
    cur = conn.cursor()             #   操作用カーソル取得
    stmt = 'SELECT * FROM books'    #   クエリの設定
    cur.execute(stmt)               #   クエリ実行
    rows = cur.fetchall()           #   実行結果を取得
    cur.close()                     #   カーソル閉じる
    conn.close()                    #   db接続解除
    return render_template('index.html', books=rows)

if __name__ == '__main__' :
    app.debug = True
    app.run()
