from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user
from datetime import datetime
from random import choice
from string import digits, ascii_letters
import os

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/recieve_photo', methods=['POST'])
@login_required
def recieve_photo():
    name_length = 30
    if (current_user.current_record == None):
        # start record
        folder = generate_random_string(name_length)
        while(os.path.exists(app.config['STORAGE_PATH'] + '/' + folder)):
            folder = generate_random_string(name_length)
        full_folder_name = app.config['STORAGE_PATH'] + '/' + folder
        os.mkdir(full_folder_name)

        # update DB
        User.query.filter_by(id=current_user.id).update(dict(current_record=folder))
        db.session.commit()

    else:
        full_folder_name = app.config['STORAGE_PATH'] + '/' + current_user.current_record

    """ post image and return the response """
    img_name = full_folder_name + '/' + datetime.now().isoformat() + '.png'
    print('NEW PHOTO '+ img_name)
    request.files['photo'].save(img_name)
    print('SAVED')
    return jsonify(status="success")

@auth.route('/stop_record')
@login_required
def stop_record():
    link = app.config['STORAGE_PATH'] + '/' + user.current_record
    User.query.filter_by(id=current_user.id).update(dict(current_record=None))
    db.session.commit()
    return render_template('stop_record.html', link = link)


def generate_random_string(length):
    symbols = ascii_letters + digits
    return ''.join(choice(symbols) for i in range(length))

