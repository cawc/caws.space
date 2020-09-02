from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from sqlalchemy import func

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User

@bp.route('/login', methods=['POST', 'GET'])
def login():
    """Login page and system"""
    if current_user.is_authenticated:
        return redirect(url_for('idea.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        return redirect(url_for('idea.index'))

    return render_template('auth/login.j2', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
