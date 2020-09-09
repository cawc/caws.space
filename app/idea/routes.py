from flask import render_template, url_for, redirect, flash
from flask_login import login_required

from sqlalchemy import func

from app import db

from app.idea import bp
from app.idea.forms import IdeaForm

from app.models import Idea

import random

@bp.route('/')
@login_required
def index():
    ideas = Idea.query.filter_by(done=False).all()

    categories = []

    for value in Idea.query.distinct(func.lower(Idea.category)).filter_by(done=False):
        categories.append(value.category)

    if len(ideas) < 1:
        return render_template('idea/index.j2', idea='No ideas available! Try adding some :)', categories=categories)
    else:
        idea = random.choice(ideas)
        return render_template('idea/index.j2', idea=f'Let\'s try: {idea.name}!', categories=categories)

@bp.route('/ideas')
@login_required
def ideas():
    ideas = Idea.query.filter_by(done=False).all()
    ideas_done = Idea.query.filter_by(done=True).all()
    return render_template('idea/ideas.j2', ideas=ideas, ideas_done=ideas_done)

@bp.route('/random/<category>')
@login_required
def random_from_category(category):
    ideas = Idea.query.filter(Idea.done==False, func.lower(Idea.category)==func.lower(category)).all()

    if len(ideas) < 1:
        return render_template('idea/random_category.j2', idea=f'No ideas for category "{category.title()}" available! Try adding some :)')
    else:
        idea = random.choice(ideas)
        return render_template('idea/random_category.j2', idea=f'[{category.title()}] Let\'s try: {idea.name}!')

@bp.route('/ideas/<idea_id>/edit', methods=['GET', 'POST'])
@login_required
def idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    form = IdeaForm(obj=idea)

    if form.validate_on_submit():
        # TODO make this dynamic
        idea.name = form.name.data
        idea.desc = form.desc.data
        idea.category = form.category.data
        idea.done = form.done.data

        db.session.add(idea)
        db.session.commit()

        flash(f'The changes to idea "{idea.name}" has been saved!')
        return redirect(url_for('idea.ideas'))

    return render_template('idea/idea_edit_form.j2', idea=idea, form=form)

@bp.route('/ideas/<idea_id>/deleteconfirmation')
@login_required
def delete_idea_confirmation(idea_id):
    idea = Idea.query.get_or_404(idea_id)

    return render_template('idea/delete_confirmation.j2', idea=idea)

@bp.route('/ideas/<idea_id>/delete')
@login_required
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)

    db.session.delete(idea)
    db.session.commit()
    flash('Idea deleted.')

    return redirect(url_for('idea.ideas'))

@login_required
@bp.route('/ideas/add', methods=['GET', 'POST'])
def add_idea():
    form = IdeaForm()

    if form.validate_on_submit():
        idea_to_add = Idea()
        form.populate_obj(idea_to_add)

        db.session.add(idea_to_add)
        db.session.commit()

        flash(f'Idea "{idea_to_add.name}" has been saved!')
        return redirect(url_for('idea.ideas'))
    
    return render_template('form_template.j2', form=form)

@bp.route('/ideas/<idea_id>/toggledone')
@login_required
def toggledone(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    idea.done = not idea.done

    db.session.add(idea)
    db.session.commit()

    return redirect(url_for('idea.ideas'))
