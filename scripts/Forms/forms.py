from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, HiddenField
from wtforms.validators import DataRequired, URL, Regexp, Length
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField('Username', validators=[Regexp(r'^[\w.@+-]+$'), Length(min=4, max=25)])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")
    password_reset = SubmitField("Forgot Password")


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class CommentForm(FlaskForm):
    comment_body = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class PasswordResetRequest(FlaskForm):
    username = StringField('Username', validators=[Regexp(r'^[\w.@+-]+$'), Length(min=4, max=25)])
    submit = SubmitField("Reset Password")


class CodeConfirm(FlaskForm):
    code_confirm = StringField('Code')
    submit = SubmitField("Submit")


class UpdatePassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MorseForm(FlaskForm):
    english = StringField("English")
    morse_code = StringField("Morse Code")
    submit = SubmitField("Convert")
    reset = SubmitField("Reset")


class AddProject(FlaskForm):
    title = StringField("Project Name", validators=[DataRequired()])
    page = StringField("Page Route", validators=[DataRequired()])
    description = CKEditorField("Project Description", validators=[DataRequired()])
    submit = SubmitField("Submit Project")
