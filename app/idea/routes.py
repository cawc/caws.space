from flask import render_template, url_for, redirect, flash
from flask_login import login_required

from app import db

from app.idea import bp
from app.idea.forms import IdeaForm

from app.models import Idea

import random

@bp.route('/')
@login_required
def index():
    ideas = Idea.query.filter_by(done=False).all()

    if len(ideas) < 1:
        return render_template('idea/index.j2', idea='No ideas available! Try adding some :)')
    else:
        idea = random.choice(ideas)
        return render_template('idea/index.j2', idea=f'Let\'s try: {idea.name}!')

@bp.route('/ideas')
@login_required
def ideas():
    ideas = Idea.query.filter_by(done=False).all()
    ideas_done = Idea.query.filter_by(done=True).all()
    return render_template('idea/ideas.j2', ideas=ideas, ideas_done=ideas_done)

@bp.route('/ideas/<idea_id>')
@login_required
def idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    return render_template('idea/idea.j2', idea=idea)

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
