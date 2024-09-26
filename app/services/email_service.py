from flask_mail import Message
from app.extensions import mail
from flask import current_app, render_template

def send_verification_email(to, token):
    msg = Message(
        subject="Verify Your Email",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to]
    )
    msg.body = render_template('email/verify_email.txt', token=token)
    msg.html = render_template('email/verify_email.html', token=token)
    mail.send(msg)

def send_password_reset_email(to, token):
    msg = Message(
        subject="Password Reset Request",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to]
    )
    msg.body = render_template('email/reset_password.txt', token=token)
    msg.html = render_template('email/reset_password.html', token=token)
    mail.send(msg)
