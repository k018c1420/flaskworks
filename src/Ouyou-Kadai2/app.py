from flask import Flask, render_template, request, redirect, session
import mysql.connector as db
import datetime
import os

db_param = {
    'user' : 'mysql',
    'host' : 'localhost',
    'password' : '',
    'database' : 'userdb'
}

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=str(session['username']))
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

if __name__ == '__main__' :
    app.debug = True
    app.run()