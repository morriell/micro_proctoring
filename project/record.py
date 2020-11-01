from flask import Blueprint, render_template, url_for, request, jsonify, send_from_directory, redirect
from flask import current_app as app
from flask_login import login_required, current_user
from .models import User, Sessions
from . import db
from datetime import datetime, timedelta
from random import choice
from string import digits, ascii_letters
import os
from hashlib import sha256
from re import match

record = Blueprint('record', __name__)

@record.route('/profile')
@login_required
def profile():
    session=''
    session_data = Sessions.query.filter_by(user=current_user.id, stop=None).first()
    if(session_data is not None):
        session=session_data.session
        session_data.stop = datetime.now()
        session_data.comment = 'Closed due to page reload'
        db.session.commit()
    return render_template('profile.html', name=current_user.name, session=session)

@record.route('/recieve_photo', methods=['POST'])
@login_required
def recieve_photo():
    current_session = Sessions.query.filter_by(user=current_user.id, stop=None).first()
    if (current_session is None):
        return jsonify(status='error', err_text='no_session')

    time_left = current_session.start \
                + timedelta(seconds=app.config['MAX_RECORD_LENGTH']) \
                - datetime.now()

    # Restrict maximum record length
    if(time_left <= timedelta(seconds=1)):
        print('TIME IS OVER')
        return jsonify(status='end_record')

    full_folder_name = app.config['STORAGE_PATH'] + '/' + current_session.session

    # Save image
    img_name = full_folder_name + '/' + datetime.now().strftime('%H-%M-%S-%d%m%y') + '.png'
    request.files['photo'].save(img_name)

    return jsonify(status="success", time_left=str(time_left).split('.').[0])

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
        new_session = Sessions(user=user, session=folder, start=datetime.now())
        db.session.add(new_session)
        db.session.commit()
    else:
        return jsonify(status="error", err_text='record_exists')
    return jsonify(status="success",
                   session=folder,
                   min_gap=app.config['PHOTO_MIN_GAP'],
                   max_gap=app.config['PHOTO_MAX_GAP'])

@record.route('/stop_record')
@login_required
def stop_record():
    session_data = Sessions.query.filter_by(user=current_user.id, stop=None).first()
    if (session_data is None):
        return jsonify(status='error')
    folder_id = session_data.session
    path = app.config['STORAGE_PATH'] + '/' + folder_id
    archive_name = path + '/' + current_user.name \
                   + '-' + datetime.now().strftime('%M-%H-%d%m%y')\
                   + '.zip'

    # Check time between photoes
    valid = True
    comment = ''
    gap = app.config['PHOTO_MAX_GAP']
    max_timedelta = timedelta(seconds=gap)
    gap_factor = app.config['GAP_FACTOR']

    photoes = os.listdir(path)
    photoes.sort(key=lambda s: os.path.getmtime(os.path.join(path,s)))
    for i in range(len(photoes)-1):
        photo = os.path.join(path, photoes[i])
        photo_next = os.path.join(path, photoes[i+1])
        time_diff = timedelta( seconds = os.path.getmtime(os.path.join(path, photoes[i+1]))
                             - os.path.getmtime(os.path.join(path, photoes[i])))
        print('DIFF: '+str(time_diff))
        if (time_diff > max_timedelta * gap_factor):
            valid = False
            #comment += photoes[i] + ' - ' + photoes[i+1]
    print('VALID: '+ str(valid))

    # Make an archive
    os.system('zip -rm ' + archive_name + ' ' + path + '/*')

    checksum = sha256(file_as_bytes(open(archive_name, 'rb'))).hexdigest()

    # Update DB
    session_data.stop = datetime.now()
    session_data.checksum = checksum
    session_data.valid = valid
    session_data.comment = comment
    db.session.commit()

    link = url_for('record.download', folder_name=folder_id, _external=True)
    print('LINK ' + link)
    print('HASH ' + checksum)

    return jsonify(status='success', link=link, hash_sum=checksum)

@record.route('/download/<folder_name>')
def download(folder_name):
    path = os.path.join(app.root_path, '../', app.config['STORAGE_PATH'], folder_name)
    files = []
    print(os.listdir(path))
    for f in os.listdir(path):
        if (match(r'.*\.zip', f)):
            files.append(f)
    print(files)
    full_path = os.path.join(path, files[0])
    if (not os.path.exists(full_path)):
        return jsonify(status='error')
    return send_from_directory(directory=path,
                               filename=files[0],
                               as_attachment=True)

def generate_random_string(length):
    symbols = ascii_letters + digits
    return ''.join(choice(symbols) for i in range(length))

def file_as_bytes(file):
    with file:
        return file.read()
