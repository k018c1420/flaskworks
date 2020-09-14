from flask import Flask, render_template, request, redirect
import mysql.connector as db
import datetime

db_param = {
    'user' : 'mysql',
    'host' : 'localhost',
    'password' : '',
    'database' : 'tododb'
}

app = Flask(__name__)

@app.route('/')
def index():
    conn = db.connect(**db_param)       #   dbと接続
    cur = conn.cursor()                 #   操作用カーソル取得
    stmt = 'SELECT * FROM todolist'        #   クエリの設定
    cur.execute(stmt)                   #   クエリ実行
    rows = cur.fetchall()               #   実行結果を取得
    cur.close()                         #   カーソル閉じる
    conn.close()                        #   db接続解除
    return render_template('Ouyou-kadai1.html', list=rows)

@app.route('/send', methods=['POST'])
def send():
    title = request.form.get('title')   #   フォームからtitle取得
    if title == "":      #   フォームが空だったら戻る
        return redirect('/')

    dt = datetime.datetime.now().strftime('%y-%m-%d %H:%M')

    conn = db.connect(**db_param)        
    cur = conn.cursor()
    
    stmt = 'SELECT * From todolist WHERE title=%s'
    cur.execute(stmt, (title,))
    rows = cur.fetchall()
    # select文の結果がなければ（入力したtitleが存在しなければ）INSERT、あればUPDATE文を実行する
    if len(rows) == 0:
        cur.execute('INSERT INTO todolist(title, date) VALUES(%s, %s)', (title, dt))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    del_list = request.form.getlist('del_list') #   削除対象のidをリスト化
    conn = db.connect(**db_param)
    cur = conn.cursor()
    stmt = 'DELETE FROM todolist WHERE id=%s'  #   列削除クエリ
    for id in del_list:
        cur.execute(stmt, (id,))    #   クエリをidのリスト全て実行
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__' :
    app.debug = True
    app.run()