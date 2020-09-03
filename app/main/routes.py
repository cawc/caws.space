from flask import render_template, redirect, url_for, flash

from app import db
from app.main import bp

@bp.route('/')
def index():
    return render_template('main/index.j2')
