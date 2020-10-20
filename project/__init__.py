from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path, mkdir, getenv
import config
from atexit import register
from shutil import rmtree
from apscheduler.schedulers.background import BackgroundScheduler

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    if (path.exists(app.config['STORAGE_PATH'])):
        print('Storage already exists.')
    else:
        mkdir(app.config['STORAGE_PATH'])

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for records
    from .record import record as record_blueprint
    app.register_blueprint(record_blueprint)

    # Schedule daily cleanup
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cleanup, args=[app.config['STORAGE_PATH']], trigger='cron', hour='2')
    scheduler.start()

    # Shut down the scheduler when exiting the app
    register(lambda: scheduler.shutdown())

    return app

def configure_app(app):
    config_names = {
        "base": "config.BaseConfig",
        "dev": "config.DevelopConfig"
    }

    try:
        app.config.from_object(config_names[getenv("CONF_NAME", "base")])
    except LookupError:
        print("Invalid configuration name. Use 'base' instead.")
        app.config.from_object(config_name['base'])

def cleanup(storage):
    return rmtree(storage + '/*')
