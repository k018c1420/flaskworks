from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message="indexページ")

@app.route('/hello/')
def hello():
    return render_template('hello.html', message="Helloページ")

if __name__ == '__main__':
    app.debug = True
    app.run()