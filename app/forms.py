from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _lazy
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired as DR, ValidationError, Email, EqualTo, Length
from app.models import User

# a strong case against my forgetful mind: certain string literals are assigned outside of a 
# request and due to that can't be affected by the client's choice of Accept-Language request header
# (eg labels associated with form fields). The way to mitigate is to find a way to delay the evaluation of
# the label strings until when they are going to be used eg until  a request for a page with forms is asked
# i think it may have an impact on response time


class LoginForm(FlaskForm):
    username = StringField(_lazy('Username', validators=[DR()]))
    password = PasswordField(_lazy('Password', validators=[DR()]))
    remember_me = BooleanField(_lazy('Remember Me'))
    submit = SubmitField(_lazy('Sign In'))




class RegistrationForm(FlaskForm):
    username = StringField(_lazy('Username', validators=[DR()]))
    email = StringField(_lazy('Email', validators=[DR(), Email()]))
    password = PasswordField(_lazy('Password', validators=[DR()]))
    password2 = PasswordField(_lazy('Repeat Password', validators=[DR(), EqualTo('password')]))
    submit = SubmitField(_lazy('Register'))


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username'))


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            # using the normal _ instead of _lazy because theis error is raised after a request(POST) is sent 
            raise ValidationError(_('Please use a different email address'))



class EditProfileForm(FlaskForm):
    username = StringField(_lazy('Username', validators=[DR()]))
    about_me = TextAreaField(_lazy('About me', validators=[Length(min=0, max=140)]))
    submit = SubmitField(_lazy('Submit'))


    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    def validate_username(self, username):
        # To make sure when user edits the username of their account, it doesn't match with a name already
        # existing in the database
        if username != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username'))



class EmptyForm(FlaskForm):
    submit = SubmitField(_lazy('Submit'))



class PostForm(FlaskForm):
    """Form for submission of blog posts"""
    post = TextAreaField(_lazy('Say something', validators=[DR(), Length(min=1, max=140)]))
    submit = SubmitField(_lazy('Submit'))


class ResetPasswordRequestForm(FlaskForm):
    """Form for password resets"""
    email = StringField(_lazy('Email', validators=[Email(), DR()]))
    submit = SubmitField(_lazy('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_lazy('Password', validators=[DR()]))
    password2 = PasswordField(_lazy('Repeat Password', validators=[DR(), EqualTo('password')]))
    submit = SubmitField(_lazy('Register'))

    


        



