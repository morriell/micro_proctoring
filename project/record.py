from flask import Blueprint, render_template, url_for, request, jsonify, send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user
from .models import User, Sessions
from . import db
from datetime import datetime
from random import choice
from string import digits, ascii_letters
import os

record = Blueprint('record', __name__)

@record.route('/recieve_photo', methods=['POST'])
@login_required
def recieve_photo():
    session = Sessions.query.filter_by(user=current_user.id).first()
    if (session is None):
        return jsonify(status='error', err_text='no_session')
    full_folder_name = app.config['STORAGE_PATH'] + '/' + session.session

    """ post image and return the response """
    img_name = full_folder_name + '/' + datetime.now().isoformat() + '.png'
    request.files['photo'].save(img_name)
    return jsonify(status="success")

@record.route('/start_record')
@login_required
def start_record():
    name_length = 30
    user = current_user.id
    current_session = Sessions.query.filter_by(user=user).first()
    if (current_session is None):
        folder = generate_random_string(name_length)
        while(os.path.exists(app.config['STORAGE_PATH'] + '/' + folder)):
            folder = generate_random_string(name_length)
        full_folder_name = app.config['STORAGE_PATH'] + '/' + folder
        os.mkdir(full_folder_name)

        # update DB
        new_session = Sessions(user=user, session=folder)
        db.session.add(new_session)
        db.session.commit()
    else:
        return jsonify(status="error", err_text='record_exists')
    return jsonify(status="success", session=folder)

@record.route('/stop_record')
@login_required
def stop_record():
    session = Sessions.query.filter_by(user=current_user.id).first()
    if (session is None):
        return jsonify(status='error')
    folder_id = session.session
    path = app.config['STORAGE_PATH'] + '/' + folder_id

    db.session.delete(session)
    db.session.commit()

    # Make a crypted archive
    os.system("gpgtar -s -o " + path + ".tar " + path)
    os.system("rm -rf " + path)
    link = url_for('record.download', id=folder_id)
    return render_template('stop_record.html', link=link)

def generate_random_string(length):
    symbols = ascii_letters + digits
    return ''.join(choice(symbols) for i in range(length))

@record.route('/download/<id>')
def download(id):
    filename = id + '.tar'
    full_path = os.path.join(app.root_path, "../" + app.config['STORAGE_PATH'])
    print(full_path)
    if (not os.path.exists(full_path)):
        return jsonify(status='error')
    return send_from_directory(directory=full_path, filename=filename, as_attachment=True)
