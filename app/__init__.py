from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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



# this is written here to avoid circular imports
from app import routes, models