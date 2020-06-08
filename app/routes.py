from app import app


@app.route('/')   # decorators can also be used as functions for callbacks
# totally unrelated point though
@app.route('/index')
def index():
    return 'hello world'