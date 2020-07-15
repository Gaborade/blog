
from app import db, login
from app import app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time


# using a many-to-many relationship model for followers
# unlike one-to-many database model which are easy to create using the already existing data tables,
# many-to-many relationships are created by creating an auxiliary table called the association table
# to create thet relationship
# Then the foreign keys of the database models are then referenced in the association table.
# In this peculiar case, the database model being referenced for the creation of the association table
# is just one database model, the User model. A situation where only the instances of a database model is used 
# for a many-to-many relationship is called a self-referential relationship
followers = db.Table('followers',
db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


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
    # referencing the one-to-many relationship for Posts in the User model class
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # referencing the many-to-many relationship for followers in the User model class
    # self-referential relationship where user instances follow other user instances
    followed = db.relationship('User', secondary=followers,
    primaryjoin=(followers.c.follower_id==id),
    secondaryjoin=(followers.c.followed_id==id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}>'


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def check_password(self, password):
        """Returns a boolean value of whether user password matched password hash or not"""

        return check_password_hash(self.password_hash, password)


    def get_reset_password_token(self, expires_in=600):
        """This method generates a token for the user for password reset to ensure that the email belongs to 
        the user. The token will be signed by being verified by the verify_password_token static method. 
        Verifying the token validates the token. The token payload is going to be in the form of 
        {'reset_password': 'user_id', 'exp': token_expiration}
        where reset password value is the id of the User and exp indicates the token expiration. If a token is past
        its expiration time, it is invlaid"""

        # the payload is always in a dictionary form
        # .decode('utf-8') because jwt.encode returns in bytes but we need it in a string format
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'].decode('utf-8'))


    @staticmethod
    def verify_reset_password_token(token):
        """This static method verifies the token. When the user clicks on the email link, the token is sent to
        the function responsible for that endpoint and the token is verified.If User is valid, then the User
        is identified by the User id"""
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'])['reset_password']
        except:
            return
        return User.query.get(id)


    def avatar(self, size):
        """Avatars are generated for users by hashing their emails using md5 and appending their hashed emails
        to gravatar url. The ?d query string parameter determines what image Gravatar provides for users in case
        they haven't registered an avatar with Gravatar. In this case we use identicon images.
        ?s query string parameter determines the size of the image"""

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()  # .encode becasue md5 works on bytes not strings
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon?s={size}'


    def follow(self, user):
        if not self.is_following(user):
            # through sqlalchemy a user following another user in the table
            # can be done as though it were a list
            self.followed.append(user)

    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)


    def is_following(self, user):
        # the filter method here unlike filter_by can contain other arbitrary filtering conditions
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


    def followed_posts(self):
        """A method which returns all the recent blog posts written by the current user's followed users and the current user herself. 
        The posts by the user's followed users are merged and then sorted by recent time. This is a computationally expensive process.
        However there is no way to bypass merging and sorting the posts. But by using indexes to query it becomes more efficient.
        Indexes scale better"""
        # the join operation creates a temporary table which merges the post and followers table data
        # the join is merged based on the condition passed as an argument ie the conditions to filter user's followed posts
        followed =  Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id==self.id)   

        # the user will also want to see her personal posts in the blog posts. 
        # To do that the user's posts are queried and are then merged with the other posts already queried using the union operation
        # then the posts are sorted based on recency 
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())  # Post.timestamp.desc() sorts the posts by time on a descending order.
        # Due to this, the most recent post will be rendered first


 
   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # no () to utcnow 
    # because it acting as first class function
    # also better to work with utc times in a server. UTC times will be converted to the user's local time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f'<Post {self.body}>'
