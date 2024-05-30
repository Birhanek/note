from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required
import json

from .models import Note
from . import note_db


views = Blueprint('views',__name__)

update_controller = False
# home
@views.route('/')
def home():
    return render_template("home.html", user = current_user)

# creating note
@views.route('/notes', methods =['POST', 'GET'])
@login_required
def notes():
    if request.method == 'POST':
        description = request.form.get('description')
        title = request.form.get('title')

        if len(description) < 1:
            flash('Description is required!', category='error')
        new_note = Note(description=description, title= title, user_id=current_user.id)
        note_db.session.add(new_note)
        note_db.session.commit()
        flash('Successfully note added', category='success')

    return render_template("notes.html", user= current_user, is_updating = update_controller)


# deleting a single note
@views.route('/note/<int:id>/delete')
@login_required
def delete_note(id):

    note = note_db.get_or_404(Note,id)
    note_db.session.delete(note)
    note_db.session.commit()

    return redirect(url_for('views.notes'))

# retrieving note
@views.route('/note/<int:id>/update')
@login_required
def update_note(id):
    note = note_db.get_or_404(Note, id)
  
    update_controller = True
    return render_template('notes.html', user=current_user, noting = note, is_updating=update_controller)

# saving an updated note 
@views.route('/note/update/<int:id>/update',methods=['POST'])
@login_required
def updating(id):
    note = note_db.get_or_404(Note, id)
    global update_controller
    description = request.form.get('description')
    title = request.form.get('title')
    note.description = description
    note.title = title
    note_db.session.commit()
    update_controller = False

    return redirect(url_for('views.notes'))




