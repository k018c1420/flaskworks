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
    return render_template('Kadai5-3.html', msgList=msgList, avg=average())

@app.route('/send', methods=['POST'])
def send():
    
    msg = request.form.get('msg')
    dt = datetime.datetime.now().strftime('%m/%d %H:%M')

    msgobj = Message(msg, dt)
    
    msgList.append(msgobj)

    return render_template('Kadai5-3.html', msgList=msgList, avg=average())

def average():
    avg = 0
    for i in msgList:
        avg = (avg + int(i.msg))
    
    if len(msgList)!= 0:
        return avg / len(msgList)
    else:
        return 0

if __name__ == '__main__' :
    app.debug = True
    app.run()