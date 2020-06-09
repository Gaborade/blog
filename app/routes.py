from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse


user = {'username' : 'Young padawan'}
posts = [
    {
        'author': {'username': 'Han Solo'},
        'body': 'Look at my great works and despair'
    },
    {
        'author': {'username': 'Alan Moore'},
        'body': 'The social vulgus listens'
    }
]

@app.route('/')   # decorators can also be used as functions for callbacks
# totally unrelated point though
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """"Login view function is responsible for authenticating users.
    Login view function also restricts certain pages from the view if user
    hasn't logged in. In such scenarios where a user attempts to access a restricted url or 
    resource, a redirect is sent to the login page for user to authenticate. If a user is blocked from access
    and is redirected to the login page and logs in, the user is sent back to the previous page that the user was
    blocked from viewing but with a caveat. The previous page is attached to redirect to original url page 
    as the value of a query string called next.
    For eg, a restricted url named '/home'. User tries to access and is sent to log in. User logs in and is redirected back
    to original page like this: '/login?next=/home'"""

    # if user has already logged in current session or set
    # remember_me to True, redirect user to main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # check if User exists or password is wrong
        user = User.query.filter_by(username=form.username.data).first()  # .first() when you need only one result
        if user is None or not user.check_password(form.password.data):
            flash('Invalide username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # checks if user is logging in from a redirection from a restricted page
        next_page = request.args.get('next')

        # if there is no next_page argument or next_page argument of url is set to a full url that contains a 
        # domain name then, redirect back to index page.
        # The reason is the next_page should just contain the relative urls of the page not the full
        # domain name. An attacker could set the next_page to the domain name of a malicious site.
        # url_parse checks if the netloc/domain component of a url is empty or not. This improves security
        # urllib.parse.urlparse could also be used

        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return (redirect(next_page))
    return render_template('login.html',title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




