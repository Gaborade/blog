from flask_mail import Message
from app import mail
from flask import render_template
from flask_babel import _
from app import app
from threading import Thread




def send_mail(subject, sender, recipients, text_body, html_body):
    """A function wrapper around flask mail"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.hmtl = html_body

    # sending emails slows down speed of app since the app runs serially.
    # this affects the response of server to other client requests 
    # To handle that, a separate thread is created in the background to handle the sending of emails
    Thread(target=send_async_mails, args=(app, msg)).start()



def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    send_mail(_('[Microblog]',
    sender=app.config['ADMINS'][0],
    recipients=[user.email],
    text_body=render_template('email/reset_password.txt', user=user, token=token),
    html_body=render_template('email/reset_password.html', user=user, token=token)
    ))


def send_async_mails(app, msg):
    # there are two types of contexts in flask, the request context and application context
    # app.app_context is the application context or the Flask instance.
    # when starting custom threads in Flask many extensions need to know their application instance
    # because they usually have their data configured with app.config. In this case, flask-mail needs the 
    # configuration of the Mail server specifications in order to run properly
    # therefore, app.app_context() creates the application context
    with app.app_context():
        mail.send(msg)
