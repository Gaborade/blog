from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
        """Flask login helps to keep track of a user's session state by storing the User's
        unique identifier in this case the User's id"""

        # the id is passed as a string but since it is an id for a database, needs to be a string
        return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # index and unique help for databse search
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}>'


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def check_password(self, password):
        """Returns a boolean value of whether user password matched password hash or not"""

        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        """Avatars are generated for users by hashing their emails using md5 and appending their hashed emails
        to gravatar url. The ?d query string parameter determines what image Gravatar provides for users in case
        they haven't registered an avatar with Gravatar. In this case we use identicon images.
        ?s query string parameter determines the size of the image"""

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()  # .encode becasue md5 works on bytes not strings
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon?s={size}'

    
   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # no () to utcnow because it acting as first class function
    # also better to work with utc times in a server. UTC times will be converted to the user's local time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f'<Post {self.body}>'
