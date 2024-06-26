# External imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required



# user Defined imports
from .models import User
from . import note_db
from .checker import check_string


auth = Blueprint('auth',__name__)

# a database query that login a user
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not '@' in email or not '.' in email:
            flash('It is not a correct email format!',category="error")
        elif len(password) < 7 and check_string(password):
            flash('password length is less than 7!', category="error")
        else:
            user = User.query.filter_by(email = email).first()
            if user:
                if user.is_banned:
                    flash('You are banned. Please contact the administrator!', category='error')
                else:  
                    if check_password_hash(user.password, password):
                        #flash('Logged in successfully!', category='success')
                        login_user(user, remember=True)
                        if user.is_admin:
                            return redirect(url_for('users.user_profile')) 
                        else:
                            return redirect(url_for( 'views.notes'))
                    else:
                        flash('Either email or password is incorrect. Try again!', category='error')
            else:
                flash('User with the email does not exist!', category='error')


    return render_template("login.html", user= current_user)

# a database query that logout a user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# a database query that register a user
@auth.route('/signup', methods = ['POST', 'GET'])
def signup():

    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password')
        c_password = request.form.get('confirmPassword')

        user = User.query.filter_by(email= email).first()
        if user:
            flash('Email exists. Try to login!',category="error")
        else:
            if not '@' in email or not '.' in email:
                flash('Your email does not contain either @ or . after the email service',category="error")
            elif len(first_name) < 2:
                flash('First name can not be less than 1 character',category="error")
            elif len(last_name) < 2:
                flash('Last name can not be less than 1 character',category="error")
            elif password1 != c_password or  len(password1) < 7 or not check_string(password1):
                flash('Password does not match! or password length is less than 7!', category="error")
            else:
                new_user = User(email = email, first_name=first_name, last_name=last_name,password=generate_password_hash( password1, method='pbkdf2:sha256'))
                note_db.session.add(new_user)
                note_db.session.commit()
                flash("Account successfully created!", category="success")
                return redirect(url_for('views.notes'))
    
    return render_template("signup.html", user = current_user)