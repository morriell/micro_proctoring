from flask import Blueprint, render_template, url_for, request, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from .models import User
from . import db
from datetime import datetime
from random import choice
from string import digits, ascii_letters
import os

record = Blueprint('record', __name__)

@record.route('/recieve_photo', methods=['POST'])
@login_required
def recieve_photo():
    if (current_user.current_record == None):
        return jsonify(status='error', err_text='no_session')
    full_folder_name = app.config['STORAGE_PATH'] + '/' + current_user.current_record

    """ post image and return the response """
    img_name = full_folder_name + '/' + datetime.now().isoformat() + '.png'
    request.files['photo'].save(img_name)
    return jsonify(status="success")

@record.route('/start_record')
@login_required
def start_record():
    name_length = 30
    if (current_user.current_record == None):
        folder = generate_random_string(name_length)
        while(os.path.exists(app.config['STORAGE_PATH'] + '/' + folder)):
            folder = generate_random_string(name_length)
        full_folder_name = app.config['STORAGE_PATH'] + '/' + folder
        os.mkdir(full_folder_name)

        # update DB
        User.query.filter_by(id=current_user.id).update(dict(current_record=folder))
        db.session.commit()
    else:
        return jsonify(status="error", err_text='record_exists')
    return jsonify(status="success", session=folder)

@record.route('/stop_record')
@login_required
def stop_record():
    link = app.config['STORAGE_PATH'] + '/' + user.current_record
    User.query.filter_by(id=current_user.id).update(dict(current_record=None))
    db.session.commit()
    return render_template('stop_record.html', link=link)

def generate_random_string(length):
    symbols = ascii_letters + digits
    return ''.join(choice(symbols) for i in range(length))

