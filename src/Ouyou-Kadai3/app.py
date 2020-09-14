from flask import Flask, render_template, request, redirect, session
import mysql.connector as db
import datetime
import os

db_param = {
    'user' : 'mysql',
    'host' : 'localhost',
    'password' : '',
    'database' : 'usertododb'
}

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        conn = db.connect(**db_param)       #   dbと接続
        cur = conn.cursor()                 #   操作用カーソル取得
        stmt = 'SELECT id, date, title FROM todolist WHERE user=%s'        #   クエリの設定
        cur.execute(stmt, (username,))                   #   クエリ実行
        rows = cur.fetchall()               #   実行結果を取得
        cur.close()                         #   カーソル閉じる
        conn.close()                        #   db接続解除
        return render_template('index.html', list=rows)
    else:
        return render_template('login.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/new', methods=['POST'])
def createUser():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == "" or pw == "":
        return redirect('/new')

    conn = db.connect(**db_param)        
    cur = conn.cursor()
    stmt = 'SELECT * From users WHERE id=%s'
    cur.execute(stmt, (id,))
    rows = cur.fetchall()

    if len(rows) == 0:
        cur.execute('INSERT INTO users(id, pw) VALUES(%s, %s)', (id, pw))
    else:
        return redirect('/new')
    conn.commit()
    cur.close()
    conn.close()

    session['username'] = request.form.get('id')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == "" or pw == "":
        return redirect('/')

    conn = db.connect(**db_param)        
    cur = conn.cursor()
    stmt = 'SELECT * From users WHERE id=%s AND pw=%s'
    cur.execute(stmt, (id, pw))
    rows = cur.fetchall()

    if len(rows) == 0:
        return redirect('/')
    else:
        session['username'] = request.form.get('id')
        return redirect('/')

@app.route('/send', methods=['POST'])
def send():
    title = request.form.get('title')   #   フォームからtitle取得
    user = session['username']
    if title == "":      #   フォームが空だったら戻る
        return redirect('/')

    dt = datetime.datetime.now().strftime('%y-%m-%d %H:%M')

    conn = db.connect(**db_param)        
    cur = conn.cursor()
    
    stmt = 'SELECT * From todolist WHERE title=%s AND user=%s'
    cur.execute(stmt, (title, user))
    rows = cur.fetchall()
    # select文の結果がなければ（入力したtitleが存在しなければ）INSERT、あればUPDATE文を実行する
    if len(rows) == 0:
        cur.execute('INSERT INTO todolist(title, date, user) VALUES(%s, %s, %s)', (title, dt, user))
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