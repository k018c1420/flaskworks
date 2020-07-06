from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')

def hello_world():
    dt = datetime.datetime.now()
    date = dt.strftime('%m/%d %H:%M')
    return date

if __name__ == '__main__':
    app.debug = True
    app.run()