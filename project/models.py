from . import db
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    authenticated = db.Column(db.Boolean, default=True)
    current_record = db.Column(db.String(30), unique=True, default=None)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_session(self):
        return self.current_record

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    session = db.Column(db.String(30), unique=True, default=None)

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    started = db.Column(db.DateTime)
    stopped = db.Column(db.DateTime)
    expire_date = db.Column(db.DateTime)

