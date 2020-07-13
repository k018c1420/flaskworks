from flask import Flask, render_template
app = Flask(__name__)

list = []

@app.route('/user/<name>/')
def profile(name):
    list.append(name)
    return render_template('Kadai4-add.html', message=name)

@app.route('/list/')
def test():
    return render_template('Kadai4-list.html', list=list)


if __name__ == '__main__':
    app.debug = True
    app.run()