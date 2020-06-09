from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # index and unique help for databse search
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}>'

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow) # no () to utcnow because it acting as first class function
    # also better to work with utc times in a server. UTC times will be converted to the user's local time
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


    def __repr__(self):
        return f'<Post {self.body}>'
