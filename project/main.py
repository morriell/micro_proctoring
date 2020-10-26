from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from . import db
from locale import setlocale, LC_ALL
from .models import Sessions, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/check')
def check():
    return render_template('check.html')

@main.route('/check_hash/<checksum>')
def check_hash(checksum):
    current_session = Sessions.query.filter_by(checksum=checksum).first()
    if (current_session is None):
        return jsonify(status='error')
    user = User.query.filter_by(id=current_session.user).first()

    # Get localized date
    setlocale(LC_ALL, ('RU','UTF8'))
    start_date = current_session.start.strftime('%d %B %Y')
    stop_date = current_session.stop.strftime('%d %B %Y')

    start_time = current_session.start.strftime('%H:%M')
    stop_time = current_session.stop.strftime('%H:%M')

    return jsonify(status='success',
                   start_date=start_date,
                   start_time=start_time,
                   stop_date=stop_date,
                   stop_time=stop_time,
                   user_name=user.name)
