from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


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
def index():
    return render_template('index.html', title='Home', user = user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return (redirect(url_for('index')))

    return render_template('forms.html',title='Sign In', form=form)



