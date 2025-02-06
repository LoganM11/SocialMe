import bcrypt
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default = False)
    accounts = db.relationship('Account', backref='user', lazy=True)


    def __init__ (self, email, name, password, is_admin = False):
        self.email = email
        self.password = password
        self.name=name
        is_admin = is_admin

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_picture = db.Column(db.LargeBinary, nullable=True)
    username = db.Column(db.String(6), nullable=False)

    def __init__ (self, profile_picture=None):
        self.profile_picture = profile_picture
        
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cookies = db.Column(db.LargeBinary, nullable=True)
    platform_number = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, username, password, platform_number, account_id, cookies=None):
        self.name = name
        self.username = username
        self.password = password
        self.platform_number = platform_number
        self.account_id = account_id
        self.cookies = cookies