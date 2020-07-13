from flask import Flask, render_template
app = Flask(__name__)

data = ["AAA", "BBB", "CCC", "DDD"]

@app.route('/post/<int:post_id>/')
def profile(post_id):
    if post_id < len(data):
        return render_template('index.html', message=data[post_id])
    else:
        return "0 ~ " + str(len(data)-1) + "の値を入力してください"


if __name__ == '__main__':
    app.debug = True
    app.run()