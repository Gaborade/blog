import os

# rather than set the configs in the main application module,
# create a separation of concerns and create a module for configuration

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # use class variables
    # secret_keys can be used as cryptographic keys, to generate tokens and signatures
    # can use secret_keys to prevent csrf attacks when filling web forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess'  # in case an environment variable secret key has not been set
    # then use a difficult secret_key in module probably with openssl

    # good to set an environment variable or a fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # configuration variables for email/smtp server
    MAIL_SERVER = os.environ.get('MAIL_SERVER') 
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) # if email port is not set in environment variable,
    # then the standard of 25 is used
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_EMAIL')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['gabdanq@gmail.com']
    POSTS_PER_PAGE = 20
    LANGUAGES = ['en', 'es', 'fr']  # i'll add translation for french later since we live francophone countries
