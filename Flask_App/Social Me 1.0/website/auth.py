from flask import Blueprint, render_template, flash
from flask import redirect, url_for, request, session
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import db
import time

from .models import User, Account, Channel

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)  # Changed session handling to Flask-Login
                flash("", category="none")
                return redirect(url_for('views.upload'))
            else:
                flash('Invalid username or password', category='error')
        else:
            flash('Invalid username or password', category='error')
            
    return render_template("login.html", email=email)

@auth.route('/logout')
@login_required  # Ensures only logged-in users can log out
def logout():
    logout_user()  # Changed session.clear() to Flask-Login's logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    email = ""
    name = ""

    if request.method == "POST":
        email = request.form.get('email').lower()
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if not email:
            flash('Please input email', category='error')
        elif not validate_email(email):
            flash('Invalid email', category='error')
        elif len(email) < 4 or len(email) > 30:
            flash('Invalid email length (4-30)', category='error') 
        elif User.query.filter_by(email=email).first():
            flash('Email already in use', category='error') 
        elif not name:
            flash('Please input name', category='error')
        elif len(name) < 2 or len(name) > 20:
            flash('Invalid name length (2-20)', category='error')    
        elif not password:
            flash('Please input password', category='error')
        elif len(password) < 8 or len(password) > 20:
            flash('Invalid password length <br> (8-20)', category='error')    
        elif password != confirm_password:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(
                email=email, 
                name=name, 
                password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            )         
            db.session.add(new_user) 
            db.session.commit()
            login_user(new_user)  # Changed session handling to Flask-Login
            flash("", category="none")
            return redirect(url_for('views.upload'))
                
    return render_template("sign-up.html", email=email, name=name)