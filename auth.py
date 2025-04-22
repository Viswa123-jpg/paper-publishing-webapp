from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import user, db
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import abort
from flask_login import current_user

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email_id']
        fullname = request.form['fullname']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        #role = request.form['role']  # admin, editor, or viewer
        new_user = user(username=username, password=password, role='user', fullname=fullname)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('registration.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        new_user = user.query.filter_by(username=request.form['email_id']).first()
        if new_user and bcrypt.check_password_hash(new_user.password, request.form['password']):
            login_user(new_user)
            session['logged_in'] = True
            session['username'] = new_user.full_name
            session['role'] = new_user.user_role
            session['email_id'] = new_user.username
            flash('Login successful!', 'success')
            if session.__contains__('url'):
                redirect_url = session['url']
                return redirect(url_for(redirect_url))
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
            return render_template('login.html', login_failed='True')
    return render_template('login.html', login_failed='False')

@auth.route('/logout')
@login_required
def logout():
    session.pop('logged_in')
    session.pop('username')
    session.pop('role')
    logout_user()
    return redirect(url_for('main.home'))

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.user_role not in roles:
                return abort(403)  # Forbidden access
            return func(*args, **kwargs)
        return decorated_view
    return wrapper