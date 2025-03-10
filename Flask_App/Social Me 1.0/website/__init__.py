from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()  # Bcrypt is now global
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'siuhweuiusloq'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    bcrypt.init_app(app)  # Initialize bcrypt with app

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Account, Channel

    # Flask-Login Setup
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Redirect unauthorized users
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load user from database

    # Flask-Session Setup
    app.config['SESSION_TYPE'] = 'filesystem'  # Stores sessions on the server
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    Session(app)  # Initialize Flask-Session

    create_database(app)
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
