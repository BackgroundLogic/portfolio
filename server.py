# Package imports
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import current_user, LoginManager, login_user, logout_user
from datetime import date
from flask_gravatar import Gravatar
import os
import psycopg2
# script imports
from scripts.mailer.mailer import Mailer, mail
from scripts.Forms.forms import ContactForm, RegisterForm, LoginForm, CreatePostForm, CommentForm, \
    PasswordResetRequest, CodeConfirm, UpdatePassword
from scripts.SQLSetup.models import db, User, Post, Comment, Reset
from scripts.Functions.func import hash_password, check_password_hash, admin_only

# setup application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
mailer = Mailer()
bootstrap = Bootstrap5(app)
lm = LoginManager()
lm.init_app(app)
gravatar = Gravatar(
                app,
                size=100,
                rating='g',
                default='retro',
                force_default=False,
                force_lower=False,
                use_ssl=False,
                base_url=None
            )

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# create or update database
with app.app_context():
    db.create_all()

# Setup Flask Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get("FROM_EMAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail.init_app(app)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', all_posts=posts, logged_in=current_user.is_authenticated)


@app.route('/cv')
def cv():
    return render_template('cv.html', logged_in=current_user.is_authenticated)


@app.route('/template')
def template():
    return render_template('blank-template.html', logged_in=current_user.is_authenticated)


@app.route('/contact_me', methods=['GET', 'POST'])
def contact_me():
    if current_user.is_authenticated:
        contact_form = ContactForm(
            name=current_user.name,
            email=current_user.email
        )
    else:
        contact_form = ContactForm()
    if contact_form.validate_on_submit():
        # leaving send function disabled until ready for release
        # mailer.contact_me(
        #     name=contact_form.name.data,
        #     email=contact_form.email.data,
        #     message=contact_form.message.data
        # )
        return render_template('contact-me.html')
    return render_template('contact-me.html', form=contact_form, logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("An account with this email already exists, use another email and try again.")
        elif register_form.password.data != register_form.confirm_password.data:
            flash("Passwords do not match, check your spelling and try again.")
        else:
            new_user = User(
                name=register_form.name.data,
                username=register_form.username.data,
                email=register_form.email.data,
                password=hash_password(register_form.password.data)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            mailer.account_registration(email=new_user.email, name=new_user.name)
            return redirect(url_for('home'))
    return render_template('register.html', form=register_form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if login_form.password_reset.data:
            return redirect(url_for('pw_reset_request'))
        elif not user:
            flash("No user with that name, try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=login_form, logged_in=current_user.is_authenticated)


@app.route("/password-reset-request", methods=['GET', 'POST'])
def pw_reset_request():
    code = 123456
    request_form = PasswordResetRequest()
    if request_form.validate_on_submit():
        user = User.query.filter_by(username=request_form.username.data).first()
        if not user:
            flash("No user with that username please check your entry and try again.")
        else:
            # mailer.password_reset(
            #     name=user.name,
            #     username=user.username,
            #     email=user.email,
            #     code=code
            # )
            new_reset = Reset(
                user_reset=user,
                code=code
            )
            db.session.add(new_reset)
            db.session.commit()
            return redirect(url_for('code_confirm', user_id=new_reset.user_id))
    return render_template("reset-request.html", code=code, form=request_form, logged_in=current_user.is_authenticated)


@app.route("/password-reset-confirm/<user_id>", methods=['GET', 'POST'])
def code_confirm(user_id):
    code_form = CodeConfirm()
    user_to_reset = Reset.query.filter_by(user_id=user_id).first()
    if code_form.validate_on_submit():
        if code_form.code_confirm.data != user_to_reset.code:
            flash("That code does not match.")
        else:
            return redirect(url_for('update_password', user_id=user_id))
    return render_template('reset-request.html', form=code_form, logged_in=current_user.is_authenticated)


@app.route('/password-update/<user_id>', methods=['GET', 'POST'])
def update_password(user_id):
    update_form = UpdatePassword()
    if update_form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        user_to_reset = Reset.query.filter_by(user_id=user_id).first()
        if update_form.password.data != update_form.confirm_password.data:
            flash("Passwords do not match, check your spelling and try again.")
        else:
            user.password = hash_password(update_form.password.data)
            db.session.commit()
            # mailer.password_update_notification(
            #     name=user.name,
            #     email=user.email,
            #     username=user.username
            # )
            db.session.delete(user_to_reset)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("reset-request.html", form=update_form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    requested_post = Post.query.get(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register in order to comment.")
            return redirect(url_for('login'))
        new_comment = Comment(
            text=comment_form.comment_body.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("view_post", post_id=requested_post.id))
    return render_template('post.html', post=requested_post, logged_in=current_user.is_authenticated, form=comment_form)


@app.route('/post_management')
@admin_only
def post_management():
    posts = Post.query.all()
    return render_template('post-management.html', all_posts=posts, logged_in=current_user.is_authenticated)


@app.route('/create_post', methods=['GET', 'POST'])
@admin_only
def create_post():
    create_post_form = CreatePostForm()
    if create_post_form.validate_on_submit():
        new_post = Post(
            title=create_post_form.title.data,
            subtitle=create_post_form.subtitle.data,
            body=create_post_form.body.data,
            img_url=create_post_form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_management'))
    return render_template('create-post.html', form=create_post_form, logged_in=current_user.is_authenticated)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    post = Post.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.title.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        post.author = current_user
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('create-post.html', form=edit_form, logged_in=current_user.is_authenticated)


@app.route('/delete-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def delete_post(post_id):
    post_to_delete = Post.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('post_management'))


if __name__ == "__main__":
    app.run()
