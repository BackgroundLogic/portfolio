from flask import Flask, render_template, request
from mailer import Mailer

app = Flask(__name__)
mailer = Mailer()

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
    msg_data = request.form
    # Below code works in test environment,
    # need to set env for deployment environment,
    # keeping disabled until ready for full site launch
    # mailer.send_mail(
    #     name=msg_data['name'],
    #     message=msg_data['message'],
    #     email=msg_data['email'],
    # )
    return render_template('message-sent.html')


if __name__ == "__main__":
    app.run()
