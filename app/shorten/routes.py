from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from app import db

from app.shorten import bp
from app.shorten.forms import ShortenURLForm

from app.models import URL
from app.utils import admin_required

@bp.route('/shorten/urls', methods=['POST', 'GET'])
@admin_required
def urls():
    urls = URL.query.all()
    return render_template('shorten/urls.j2', urls=urls)

@bp.route('/shorten/create_url', methods=['POST', 'GET'])
@admin_required
def create_url():
    form = ShortenURLForm()

    if form.validate_on_submit():
        if URL.query.get(form.token.data) is not None:
            flash(f'Token {form.token.data} is already in use')
            return redirect(url_for('shorten.create_url'))
        shortened_url = URL(token=form.token.data, url=form.url.data)
        db.session.add(shortened_url)
        db.session.commit()
        return redirect(url_for('shorten.urls'))

    return render_template('form_template.j2', form=form)

@bp.route('/s/<token>')
def redirect_url(token):
    destination = URL.query.get_or_404(token)
    destination.clicks += 1
    db.session.add(destination)
    db.session.commit()
    return redirect(destination.url)
