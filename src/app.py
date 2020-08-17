from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as db
import os

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

@app.route('/send', methods=['POST'])
def send():
    title = request.form.get('title')   #   フォームからtitle取得
    price = request.form.get('price')   #   フォームからprice取得
    image = request.files['img_file']
    if title == "" or price == "":      #   フォームが空だったら戻る
        return redirect('/')

    if image and allowed_file(image.filename):  #   許可された拡張子であれば画像を保存
        image.save('static/uploads/' + image.filename)
    conn = db.connect(**db_param)       
    cur = conn.cursor()
    
    stmt = 'SELECT * From list WHERE title=%s'
    cur.execute(stmt, (title,))
    rows = cur.fetchall()
    # select文の結果がなければ（入力したtitleが存在しなければ）INSERT、あればUPDATE文を実行する
    if len(rows) == 0:
        cur.execute('INSERT INTO list(title, price, image) VALUES(%s, %s, %s)', (title, int(price), image.filename))
    else:
        cur.execute('UPDATE list SET price=%s, image=%s WHERE title=%s', (int(price), title, image.filename))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    del_list = request.form.getlist('del_list') #   削除対象のidをリスト化
    conn = db.connect(**db_param)
    cur = conn.cursor()
    for id in del_list:
        stmt = 'SELECT * FROM list WHERE id=%s'  #   列削除クエリ
        cur.execute(stmt, (id,))               #   クエリをidのリスト全て実行
        rows = cur.fetchall()
        os.remove('./static/uploads/' + rows[0][3])
        stmt = 'DELETE FROM list WHERE id=%s'
        cur.execute(stmt, (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/data', methods=['GET'])
def data():
    keyword = request.args.get('keyword')
    conn = db.connect(**db_param)
    cur = conn.cursor()
    if keyword and keyword != "":
        stmt = 'SELECT * FROM list WHERE title LIKE %s'
        cur.execute(stmt, ('%'+keyword+'%',))
    else:
        stmt = 'SELECT * FROM list'
        cur.execute(stmt)
    rows = cur.fetchall()
    url = 'http://127.0.0.1:5000/static/uploads/'   # <-
    data = []
    for id, title, price, image in rows:
        data.append({'id':id, 'title':title, 'price':price, 'image':url+image})
    ret = jsonify({"result":data})
    return ret



if __name__ == '__main__' :
    app.debug = True
    app.run()
