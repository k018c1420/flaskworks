from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Kadai5-1-index.html')

@app.route('/send', methods=['POST'])
def send():
    msgName = request.form.get('msg_name')
    msgMail = request.form.get('msg_mail')

    return render_template('Kadai5-1-receive.html', msgName=msgName, msgMail=msgMail)

if __name__ == '__main__' :
    app.debug = True
    app.run()
