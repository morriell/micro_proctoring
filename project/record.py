from flask import Blueprint, render_template, url_for, request, jsonify, send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user
from .models import User, Sessions
from . import db
from datetime import datetime
from random import choice
from string import digits, ascii_letters
import os
from shutil import make_archive, rmtree
from hashlib import sha224

record = Blueprint('record', __name__)

@record.route('/recieve_photo', methods=['POST'])
@login_required
def recieve_photo():
    current_session = Sessions.query.filter_by(user=current_user.id, stop=None).first()
    if (current_session is None):
        return jsonify(status='error', err_text='no_session')
    full_folder_name = app.config['STORAGE_PATH'] + '/' + current_session.session

    """ post image and return the response """
    img_name = full_folder_name + '/' + datetime.now().isoformat() + '.png'
    request.files['photo'].save(img_name)
    return jsonify(status="success")

@record.route('/start_record')
@login_required
def start_record():
    name_length = 30
    user = current_user.id
    current_session = Sessions.query.filter_by(user=user, stop=None).first()
    if (current_session is None):
        folder = generate_random_string(name_length)
        while(os.path.exists(app.config['STORAGE_PATH'] + '/' + folder)):
            folder = generate_random_string(name_length)
        full_folder_name = app.config['STORAGE_PATH'] + '/' + folder
        os.mkdir(full_folder_name)

        # update DB
        new_session = Sessions(user=user, session=folder, start=datetime.utcnow())
        db.session.add(new_session)
        db.session.commit()
    else:
        return jsonify(status="error", err_text='record_exists')
    return jsonify(status="success", session=folder)

@record.route('/stop_record')
@login_required
def stop_record():
    session_data = Sessions.query.filter_by(user=current_user.id, stop=None).first()
    if (session_data is None):
        return jsonify(status='error')
    folder_id = session_data.session
    path = app.config['STORAGE_PATH'] + '/' + folder_id

    # Make an archive
    os.system('zip -rm '+ path + '.zip ' + path)

    checksum = sha224(file_as_bytes(open(path+'.zip', 'rb'))).hexdigest()

    # Update DB
    session_data.stop = datetime.utcnow()
    session_data.checksum = checksum
    db.session.commit()

    link = url_for('record.download', id=folder_id)
    return render_template('stop_record.html', link=link, hash_sum=checksum)

def generate_random_string(length):
    symbols = ascii_letters + digits
    return ''.join(choice(symbols) for i in range(length))

@record.route('/download/<id>')
def download(id):
    filename = id + '.zip'
    full_path = os.path.join(app.root_path, "../" + app.config['STORAGE_PATH'])
    if (not os.path.exists(full_path)):
        return jsonify(status='error')
    return send_from_directory(directory=full_path, filename=filename, as_attachment=True)

def file_as_bytes(file):
    with file:
        return file.read()
