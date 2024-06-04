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

@profile.route('/user/update/<int:id>')
@login_required
def get_user_to_update(id):
    my_user = note_db.get_or_404(User,id)
    update_controller = True

    return render_template('dashboard.html', user = current_user, category=mapper, retrieved = my_user, is_updating=update_controller)

@profile.route('/user/update/<int:id>/<int:word>', methods=['POST'])
@login_required
def user_to_update(id, word):
    my_user = note_db.get_or_404(User,id)
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
    


        


@profile.route('/get-all-notes')
@login_required
def get_all_notes():
    global mapper
    mapper = "notes"
    all_notes = Note.query.all()

    return render_template("dashboard.html", category = mapper, user= current_user, notes = all_notes)