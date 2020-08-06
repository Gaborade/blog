from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_babel import Babel, _, lazy_gettext as _lazy
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os


# since we will be creating larger applications than normal better to 
# create a sub-package and initialise flask in the __init__ file


# The __name__ variable passed to the Flask class is a Python predefined variable, 
#  which is set to the name of the module in which it is used
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
# with bootstrap initialised, a bootstrap/base.html becomes available
# and can be used using the extend jinja statement clause
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)   # for language translation

# certain pages are restricted unless user logs in
# in order to accomplish that, the view function responsible for login
# is supplied to the LoginManager.login_view attribute as a string
login.login_view = 'login'
login.login_message = _lazy('Please log in to access this page')


@babel.localeselector
def get_locale():
    """ get_locale will choose based on the Accept-Language request header
        request.accept_laguages is an interface that will access the Accept-Header
        caveat here, the Accept-Header like most of the headers under Content-Negotiation
        has a certain feature called weighted list where diferent languages can be added for server to use but
        within a weighted example eg 
        Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5
        with a higher value meaning a higher preference by the client, thus in this case if server supports french
        then french first, then english and so forth.
        best_match finds the languages provided by the client's/browser's request header and compares against languages
        that the application/site supports with the weighted list(if provided) and returns the best choice
    """  
    
    return request.accept_languages.best_match(app.config['LANGUAGES'])






# ---------------------------LOGS---------------------------------------------------------
""" The basic premise for logs is that it records the activities of the server in production mode.
When product is in development mode, it is being tested locally. This generally means
debug has been set to True(by an environment variable or otherwise). In production mode, 
debug is set to False. Under a scenario where site is in production mode, 
file logs and email logs should be configured in this order of severity:
Email logs should send logs to the administrators of the site immediately an errror occurs on the site
for immediate fixing ie. logging.ERROR level. The file logs are set to logging.INFO level """



#-----------------------------------------------------------------------------------------
#                      FILE LOGGING
#-----------------------------------------------------------------------------------------

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
        # RotatingFileHandler logs rotates the logs and ensures that logs do not grow large in size(10kb in this case)
        # the last ten log files are backups
    file_handler = RotatingFileHandler('logs/microlog.py', maxBytes=10240, backupCount=10)
    # the logging format for files are in this order: timestamp, logging level, message, sourcefile and line number of log entry
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(messages) in [%(pathname)s: %(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')



#-------------------------------------------------------------------------------------------
#                SMTP LOGGING(FOR ONLY ERRORS)
#-------------------------------------------------------------------------------------------

#  An SMTP handler class from logging module then sends all errors in production code to the addresses
#  of site maintainers
# The log errors are only sent by mail if the environment variables for the mail server have been set
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        # in case mail authentication is supplied, optional though
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            # the use of a tuple for TLS is specified in Python documentation for SMTPHandler that in verbatim
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
