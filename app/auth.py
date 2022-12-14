import re
import uuid as uuid
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

from .models import User

auth =  Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.form.get('action') == 'Sign in':
        login = request.form.get('login')
        password = request.form.get('password')

        user_email = User.query.filter_by(email=login.lower()).first()
        user_username = User.query.filter_by(username=login.lower()).first()

        if user_email:
            if check_password_hash(user_email.password, password):
                login_user(user_email, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(f'Incorrect password!', category='error')
        
        elif user_username:
            if check_password_hash(user_username.password, password):
                login_user(user_username, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(f'Incorrect password!', category='error')

        else:
            flash(f'User doesn\'t exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    if request.form.get('action') == 'Sign up':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,20}$'
        match_re = re.compile(reg)
        res = re.search(match_re, password1)
        username_lowercase = username.lower()
        user = User.query.filter_by(email=email).first()

        if user:
            flash(f'User already exists with email: {email}', category='error')
        elif db.session.query(db.exists().where(User.username == username_lowercase)).scalar():
            flash(f'User already exists with username: {username}', category='error')
        elif ' ' in username:
            flash('Can\'t have space in username.', category='error')
        elif not res:
            flash('Password must have 12 characters, 1 uppercase, 1 lowercase, 1 number, '
                'and 1 special character!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            new_user = User(email=email, last_name=last_name, first_name=first_name, creation_date=date, 
            username=username_lowercase, password=generate_password_hash(password1, method='sha256'))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    '''Utilized to logout the current user. They will then be redirected back to the login/signup pages.'''
    logout_user()
    return redirect(url_for('auth.login'))
