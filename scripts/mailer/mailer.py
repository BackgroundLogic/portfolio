import os
from flask_mail import Mail, Message

mail = Mail()


class Mailer:

    def __init__(self):
        self.FROM_EMAIL = os.environ.get("FROM_EMAIL")
        self.EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
        self.ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

    def contact_me(self, name, message, email):
        msg = Message(
            f'New message from {name}',
            sender=self.FROM_EMAIL,
            recipients=[self.ADMIN_EMAIL, email]
        )
        msg.html = message
        # html used as ckeditor outputs text entry as html,
        # this way the email client doesn't render the html tags
        mail.send(msg)

    def password_reset(self, name, username, email, code):
        msg = Message(
            f'Password Reset Requested',
            sender=self.FROM_EMAIL,
            recipients=[email]
        )
        msg.html = f"""
                    <p>Hello {name}, a password reset has been requested for your account with<br />
                    Username: {username}</p>
                    <p>To change your email use this code {code}&nbsp;</p>
                    <p>If this was not you disregard this email no changes will be made to your account.</p>
        """
        mail.send(msg)

    def password_update_notification(self, name, username, email):
        msg = Message(
            f'Password Updated',
            sender=self.FROM_EMAIL,
            recipients=[email]
        )
        msg.html = f"""
                    <p>Hello {name}, your password for {username} has been updated.</p>
        """
        mail.send(msg)

    def account_registration(self, email, name):
        msg = Message(
            f'Welcome to my Portfolio Blog!',
            sender=self.FROM_EMAIL,
            recipients=[email]
        )
        msg.html = f"""
                   <p>Hello {name},</p>

                    <p>Thank you for joining my blog, really the only thing you can do is post comments on the posts I make here, this site is still heavily a work in progress and the site database may be deleted at anytime for resets/upgrades/purges, but I&#39;m glad to have you here.</p>

                    <p>Jan Olson</p>
        """