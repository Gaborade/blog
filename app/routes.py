from app import app
from flask import render_template


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

