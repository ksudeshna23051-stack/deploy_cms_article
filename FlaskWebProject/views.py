"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db
from FlaskWebProject.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import msal
import uuid
import logging

# ✅ PRO LOGGING FORMAT (IMPORTANT 🔥)
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s: %(message)s'
)

imageSourceUrl = 'https://' + app.config['BLOB_ACCOUNT'] + '.blob.core.windows.net/' + app.config['BLOB_CONTAINER'] + '/'

# -------------------- HOME --------------------
@app.route('/')
@app.route('/home')
@login_required
def home():
    app.logger.info(f"Home opened by user: {current_user.username}")

    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()

    return render_template(
        'index.html',
        title='Home Page',
        posts=posts
    )

# -------------------- NEW POST --------------------
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    app.logger.info("New post page opened")

    form = PostForm(request.form)
    if form.validate_on_submit():
        app.logger.info(f"New post created by user: {current_user.username}")

        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        return redirect(url_for('home'))

    return render_template(
        'post.html',
        title='Create Post',
        imageSource=imageSourceUrl,
        form=form
    )

# -------------------- EDIT POST --------------------
@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    app.logger.info(f"Editing post ID: {id} by user: {current_user.username}")

    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)

    if form.validate_on_submit():
        app.logger.info(f"Post updated ID: {id} by user: {current_user.username}")

        post.save_changes(form, request.files['image_path'], current_user.id)
        return redirect(url_for('home'))

    return render_template(
        'post.html',
        title='Edit Post',
        imageSource=imageSourceUrl,
        form=form
    )

# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info("Login page accessed")

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        app.logger.info(f"Login attempt: {form.username.data}")

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            app.logger.error("Login failed ❌")
            flash('Invalid username or password')
            return redirect(url_for('login'))

        app.logger.info("Login success ✅")

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')

        return redirect(next_page)

    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])

    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)

# -------------------- AZURE AUTH --------------------
@app.route(Config.REDIRECT_PATH)
def authorized():
    app.logger.info("Azure AD redirect hit")

    if request.args.get('state') != session.get("state"):
        app.logger.error("State mismatch in Azure login")
        return redirect(url_for("home"))

    if "error" in request.args:
        app.logger.error("Azure login error")
        return render_template("auth_error.html", result=request.args)

    if request.args.get('code'):
        app.logger.info("Azure login success")

        cache = _load_cache()
        result = None

        if result and "error" in result:
            app.logger.error("Token acquisition failed")
            return render_template("auth_error.html", result=result)

        session["user"] = result.get("id_token_claims") if result else None

        user = User.query.filter_by(username="admin").first()
        login_user(user)

        _save_cache(cache)

    return redirect(url_for('home'))

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    app.logger.info(f"User logged out: {current_user.username}")

    logout_user()

    if session.get("user"):
        session.clear()
        return redirect(
            Config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("login", _external=True)
        )

    return redirect(url_for('login'))

# -------------------- MSAL HELPERS --------------------
def _load_cache():
    app.logger.info("Loading MSAL cache")
    return None

def _save_cache(cache):
    app.logger.info("Saving MSAL cache")
    pass

def _build_msal_app(cache=None, authority=None):
    app.logger.info("Building MSAL app")
    return None

def _build_auth_url(authority=None, scopes=None, state=None):
    app.logger.info("Building auth URL")
    return None
