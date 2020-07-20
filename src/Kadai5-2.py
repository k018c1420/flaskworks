from flask import Flask, render_template, request
import datetime
app = Flask(__name__)
msgList = []
class Message(object):
    def __init__(self, msg, dt):
        self.msg = msg
        self.dt = dt

@app.route('/')
def index():
    return render_template('Kadai5-2.html', msgList=msgList)

@app.route('/send', methods=['POST'])
def send():
    
    msg = request.form.get('msg')
    dt = datetime.datetime.now().strftime('%m/%d %H:%M')

    msgobj = Message(msg, dt)

    msgList.append(msgobj)

    return render_template('Kadai5-2.html', msgList=msgList)

if __name__ == '__main__' :
    app.debug = True
    app.run()
