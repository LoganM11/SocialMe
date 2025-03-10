from . import db
from flask_login import UserMixin

class File_Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # Cascade deletes: deleting a User will delete associated Accounts
    accounts = db.relationship(
        'Account',
        backref='user',
        lazy=True,
        cascade="all, delete, delete-orphan"
    )

    def __init__(self, email, name, password):
        self.email = email
        self.password = password
        self.name = name

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Set ondelete='CASCADE' so the database handles cascading deletes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    account_name = db.Column(db.String(150), nullable=False)
    # Cascade deletes: deleting an Account will delete associated Channels
    channels = db.relationship(
        'Channel',
        backref='account',
        lazy=True,
        cascade="all, delete, delete-orphan"
    )

    def __init__(self, account_name, user_id):
        self.account_name = account_name
        self.user_id = user_id
        
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Set ondelete='CASCADE' to ensure channels are deleted when the Account is deleted
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    channel_name = db.Column(db.String(150), nullable=False)
    channel_cookies = db.Column(db.String(300), nullable=True)
    platform_number = db.Column(db.Integer, nullable=False)
    pword = db.Column(db.String(150), nullable=False)
    uname = db.Column(db.String(150), nullable=False)
    
    def __init__(self, channel_name, platform_number, account_id, channel_cookies, uname, pword):
        self.channel_name = channel_name
        self.platform_number = platform_number
        self.account_id = account_id
        self.channel_cookies = channel_cookies
        self.pword = pword
        self.uname = uname
