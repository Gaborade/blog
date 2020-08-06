from app import app, db, cli # microblog.py is the main application module
from app.models import User, Post


@app.shell_context_processor  # adding some pre-imports to shell whenever flask shell is used to test out stuff
def make_shell_context():
    return {'db' : db, 'User': User, 'Post': Post}


