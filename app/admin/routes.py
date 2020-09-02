from flask import render_template, redirect, url_for, flash

from sqlalchemy import func

from app import db
from app.admin import bp
from app.admin.forms import RegisterForm
from app.models import User
from app.utils import admin_required

@bp.route('/')
@admin_required
def index():
    return render_template('admin/index.j2')

@bp.route('/usermanagement')
@admin_required
def usermanagement():
    users = User.query.all()
    return render_template('admin/usermanagement.j2', users=users)

@bp.route('/register', methods=['POST', 'GET'])
@admin_required
def register():
    """Register a user"""
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
        if user is not None:
            flash(f'Username "{form.username.data}" already exists')
            return redirect(url_for('admin.register'))
        user_object = User(username=form.username.data)
        user_object.set_password(form.password.data)
        db.session.add(user_object)
        db.session.commit()
        flash('User created succesfully')
        return redirect(url_for('admin.register'))

    return render_template('form_template.j2', form=form)
