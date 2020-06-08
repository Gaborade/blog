from flask import Flask

# since we will be creating larger applications than normal better to 
# create a sub-package and initialise flask in the __init__ file

# The __name__ variable passed to the Flask class is a Python predefined variable, 
#  which is set to the name of the module in which it is used
app = Flask(__name__)


# this is written here to avoid circular imports
from app import routes