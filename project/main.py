from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Sessions, User

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
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

    # Get date
    start_date = current_session.start.strftime('%d.%m.%Y')
    stop_date = current_session.stop.strftime('%d.%m.%Y')

    start_time = current_session.start.strftime('%H:%M')
    stop_time = current_session.stop.strftime('%H:%M')

    return jsonify(status='success',
                   start_date=start_date,
                   start_time=start_time,
                   stop_date=stop_date,
                   stop_time=stop_time,
                   user_name=user.name,
                   valid=current_session.valid)

@main.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')
