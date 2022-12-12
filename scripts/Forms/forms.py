from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import data_required, URL
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[data_required()])
    email = EmailField("Email", validators=[data_required()])
    message = CKEditorField("Message", validators=[data_required()])
    submit = SubmitField("Submit")
