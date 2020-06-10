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


        



