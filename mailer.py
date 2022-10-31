import os
import smtplib


class Mailer:

    def __init__(self):
        self.FROM_EMAIL = os.environ.get("FROM_EMAIL")
        self.EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    def send_mail(self, subject, message, contact_email):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(
                user=self.FROM_EMAIL,
                password=self.EMAIL_PASSWORD,
            )
            to_emails = f"jangolson@outlook.com; {contact_email}"
            connection.sendmail(
                from_addr=self.FROM_EMAIL,
                to_addrs=to_emails,
                msg=f"Subject:{subject}\n\n{message}"
            )
