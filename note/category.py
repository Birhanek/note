# External imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required

# internal imports
from .models import Categories
from . import note_db


category = Blueprint('categories',__name__)

is_category_updating = False

# fetching all the categories
@category.route('/get-all-categories')
@login_required
def get_all_category():
    mapper = 'categories'
    all_category = Categories.query.all()
    print(all_category)
    return render_template("dashboard.html", all_catagories = all_category, category_update = is_category_updating, category= mapper, user=current_user)


# creating a category
@category.route('/category-added', methods=['POST','GET'])
@login_required
def create_category():
    if request.method == 'POST':
        category_name = request.form.get('name')
        category_description = request.form.get('description')

        if len(category_name) == 0 or len(category_description) == 0:
            flash('Either category name or category description is not inserted!', category="error")
        else:
            new_category = Categories(category_name = category_name, category_description = category_description)

            note_db.session.add(new_category)
            note_db.session.commit()

            return redirect(url_for('categories.get_all_category'))

# Updating a category
@category.route('/update/<int:id>')
@login_required
def get_category_to_update(id):
    my_category = Categories.query.filter_by(category_id=id).first_or_404()
    mapper = "categories"
    is_category_updating = True

    return render_template('dashboard.html', user = current_user, category=mapper, my_categories = my_category, category_updating=is_category_updating)

# updating 
@category.route('/update/<int:id>/<int:category_num>', methods=['POST'])
@login_required
def update_category(id,category_num):
    my_category = Categories.query.filter_by(category_id=id).first_or_404()

    name = request.form.get('name')
    description = request.form.get('description')

    my_category.category_name = name
    my_category.category_description = description

    note_db.session.commit()
    return redirect(url_for('categories.get_all_category'))

# deleting a category
@category.route('/delete/<int:id>')
@login_required
def delete_category(id):

    deleting_category = Categories.query.filter_by(category_id = id).first_or_404()
    note_db.session.delete(deleting_category)
    note_db.session.commit()

    return redirect(url_for('categories.get_all_category'))