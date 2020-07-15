from app import app, db 
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime



@app.before_request  # before request decorator makes this function execute right before the view_function
def before_request():
    if current_user.is_authenticated:
        # record last_seen field of user
        current_user.last_seen = datetime.utcnow()
        db.session.commit()




@app.route('/', methods=['GET', 'POST'])   # decorators can also be used as functions for callbacks
# totally unrelated point though
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # page variable tells page number to display. Page 1 as default
    page = request.args.get('page', 1, type=int)
    # NB: Pagination returns pagination objects. This means they are not iterable unless you attach a .items attribute in this case
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)  # boolean refers to the error flag
    next_url = url_for('index', page=posts.next_num) if page.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if page.has_prev else None
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(body=post_form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        # sidenote: better to use redirects for POST requests
        # This is to prevent duplicate insertions/submissions of the same post request
        # this practice is aptly valled the POST/redirect/GET pattern
        # The reason is to avoid certain problems which happen due to the refresh button on browsers
        # when say we submit a post request and hit the refresh button, the refresh button reissues the last request
        # which in this case is the POST request. This creates the illusion that our post didn't actually submit
        # meanwhile it did. To not cause this, we rather use a redirect which sets it to a GET request and removes the illusion 
        # which thereby prevents us from submitting already submitted POST requests
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', posts=posts.items, form=post_form, 
    next_url=next_url, prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    # if you use keyword arguments in url_for and the names of those arguments are not referenced directly in URL,
    # Flask uses that keyword as a query string as we intend to do here ie for eg /explore?page=3
    next_url = url_for('explore', page=all_posts.next_num) if page.has_next else None
    prev_url = url_for('explore', page=all_posts.prev_num) if page.has_prev else None
    
    # reuses index template which is used for home page as explore pages too
    return render_template('index.html', title='Explore', posts=all_posts.items,
    next_url=next_url, prev_url=prev_url)



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
    to original page like this: '/login?next=/home' """

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



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return url_for('index')
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(username=registration_form.username.data, email=registration_form.email.data)
        user.set_password(registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to the League of Rogues and Bandits! Let the end begin')  # what of goths and bots
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registration_form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    # the user profile page will only display posts created by the user himself
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'],
    False)
    next_url = url_for('user', username=user.username, page=posts.next_num)  \
        if page.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if page.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items, form=form, next_url=next_url,
    prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = EditProfileForm(current_user.username)
    if edit_form.validate_on_submit():
        current_user.username = edit_form.username.data
        current_user.about_me = edit_form.about_me.data
        db.session.commit()
        flash('Your changes have been made')
        return redirect(url_for("edit_profile"))
        # when user initially requests for edit_profile.html page,
        # repopulate fields with current data already stored in the database
    elif request.method == 'GET':
            edit_form.username.data = current_user.username
            edit_form.about_me.data = current_user.about_me
    # else if user makes a mistake with submission of forms just return page back to user
    return render_template('edit_profile.html', title='Edit Profile', form=edit_form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    """Although it may seem that a function that basically lets user follow other users
    should be implemented as a a GET request, there needs to be another afterthought. Follow action introduces
    change into the application. It would be easier to implement this as a GET request but it also 
    makes it harder to protect it against CSRF attacks. So we'll use a Form to implement the follow action as a POST 
    request. As a rule of thumb, any action that introduces change in the application, should be implemented as a POST request
    and actions that don't cause any change in the app, GET requests"""
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'{user} not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself')
            return (redirect(url_for('user', username=username)))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {user}')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    """Unfollow function will follow a similar approcah to follow function"""
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself')
            return (redirect(url_for('user', username=username)))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You unfollowed {user}')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))






@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
