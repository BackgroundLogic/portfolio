from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from scripts.mailer.mailer import Mailer
from scripts.Forms.forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sHHSssHHsUPERSecretKeyrIGHThere'
ckeditor = CKEditor(app)
mailer = Mailer()
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/template')
def template():
    return render_template('blank-template.html')


@app.route('/contact_me', methods=['GET', 'POST'])
def contact_me():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        # leaving send function disabled until ready for release
        # mailer.send_mail(
        #     name=contact_form.name.data,
        #     email=contact_form.email.data,
        #     message=contact_form.message.data
        # )
        return render_template('contact_me.html')
    return render_template('contact_me.html', form=contact_form)


if __name__ == "__main__":
    app.run(debug=True)
