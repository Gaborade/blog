from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired as DR, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DR()])
    password = PasswordField('password', validators=[DR()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DR()])
    email = StringField('Email', validators=[DR(), Email()])
    password = PasswordField('Password', validators=[DR()])
    password2 = PasswordField('Repeat Password', validators=[DR(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')



class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DR()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    def validate_username(self, username):
        # To make sure when user edits the username of their account, it doesn't match with a name already
        # existing in the database
        if username != self.original_username:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                raise ValidationError('Please use a different username')



class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')





        



