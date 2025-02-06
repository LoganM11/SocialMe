from flask import Blueprint, render_template
from flask import redirect, url_for, session
from flask import request, jsonify, flash
from .models import User, Account, Channel

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/donate')
def donate():
    return redirect(url_for("views.home"))

@views.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in first", category="error")
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)

    if not user:
        flash("User not found", category="error")
        return redirect(url_for('auth.login'))
    
    return render_template("dashboard.html", user=user)