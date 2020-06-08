from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired as DR


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DR()])
    password = PasswordField('password', validators=[DR()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




