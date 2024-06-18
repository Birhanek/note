from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# users defined imports
from .models import User, Note
from .checker import check_string
from . import note_db


profile = Blueprint('users',__name__)

update_controller = False
mapper = "users"

# a user endpoint
@profile.route('/profile')
@login_required
def user_profile():
    all_users = User.query.all()
    mapper = "users"
    return render_template("dashboard.html", category = mapper, user=current_user, all_note_users = all_users, is_updating = update_controller)

# Preparing a user to be updated
@profile.route('/user/update/<int:id>')
@login_required
def get_user_to_update(id):
    my_user = User.query.filter_by(id=id).first_or_404()
    update_controller = True

    return render_template('dashboard.html', user = current_user, category=mapper, retrieved = my_user, is_updating=update_controller)

# updating a user
@profile.route('/user/update/<int:id>/<int:word>', methods=['POST'])
@login_required
def user_to_update(id, word):
    my_user = User.query.filter_by(id=id).first_or_404()
    global update_controller
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    password = request.form.get('password')
    if len(password) < 7 or not check_string(password):
        flash("Password requirement failure! try with strong password", category="error")
    elif len(first_name) < 2:
        flash('First name can not be less than 1 character',category="error")
    elif len(last_name) < 2:
        flash('Last name can not be less than 1 character',category="error")
    else:
        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.password = generate_password_hash( password, method='pbkdf2:sha256')
        note_db.session.commit()

        update_controller = False
    return redirect (url_for("users.user_profile"))
    
# deleting a single user
@profile.route('/user/banned/<int:id>')
@login_required
def banned_user(id):

    # note = note_db.get_or_404(Note, id)
    banning_user = User.query.filter_by(id=id).first_or_404()
    if banning_user.is_banned:
        banning_user.is_banned = False
    else:
        banning_user.is_banned = True
    note_db.session.commit()

    return redirect(url_for('users.user_profile'))

        

# Fetch all notes
@profile.route('/get-all-notes')
@login_required
def get_all_notes():
    global mapper
    mapper = "notes"
    all_notes = Note.query.all()

    return render_template("dashboard.html", category = mapper, user= current_user, notes = all_notes)