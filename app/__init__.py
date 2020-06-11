from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler
import logging

# since we will be creating larger applications than normal better to 
# create a sub-package and initialise flask in the __init__ file


# The __name__ variable passed to the Flask class is a Python predefined variable, 
#  which is set to the name of the module in which it is used
app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# certain pages are restricted unless user logs in
# in order to accomplish that, the view function responsible for login
# is supplied to the LoginManager.login_view attribute as a string
login.login_view = 'login'



# if debug is True, then server is in development mode and being tested locally.
# However if debug is set to False, then this means this is production code. An SMTP handler class
# from logging module then sends all errors in production code to the addresses of site maintainers
# The log errors are only sent by mail if the environment variables for the mail server have been set
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            # the use of a tuple for TLS specified in Python documentation for SMTPHandler that in verbatim
            # "To specify the use of a secure protocol (TLS), pass in a tuple
            #  to the secure argument. This will only be used when authentication
            #  credentials are supplied. The tuple should be either
            #  an empty tuple, or a single-value tuple with the name of a keyfile, or a 2-value
            #  tuple with the names of the keyfile and certificate file. "
            secure = ()
        mail_handler =SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='noreply@' + app.config['MAIL_SERVER'], toaddrs=app.config['ADMINS'], subject='Microblog failure',
        credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)  # only error level logs should be sent, not info, critical warnings or debug messages
        app.logger.addHandler(mail_handler)





# this is written here to avoid circular imports
from app import routes, models, errors