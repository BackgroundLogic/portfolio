from flask import Flask, render_template
from mailer import Mailer

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/template')
def template():
    return render_template('blank-template.html')


@app.route('/message_sent', methods=['POST'])
def message_sent():
    return render_template('message-sent.html')


if __name__ == "__main__":
    app.run()
