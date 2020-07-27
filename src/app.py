from flask import Flask, render_template, request
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../static/uploads/'  #flaskworks/srcの中にapp.pyがある為、../static...にしている

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    img_file = request.files['img_file']
    if img_file and allowed_file(img_file.filename):
        img_file.save(app.config['UPLOAD_FOLDER'] + img_file.filename)
        return '<p>画像' + img_file.filename + 'を送信しました</p>'
    else:
        return '<p>許可されていない拡張子です</p>'

if __name__ == '__main__' :
    app.debug = True
    app.run()
