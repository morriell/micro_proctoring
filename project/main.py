from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from . import db
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
    return jsonify(status='success',
                   start_date=current_session.start,
                   end_date=current_session.stop,
                   user_name=user.name)
