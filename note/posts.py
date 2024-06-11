# External imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required

# internal imports
from .models import Posts, User
from . import note_db

posts = Blueprint('posts', __name__)
is_post_updating = False

# fetching all posts
@posts.route('/')
@login_required
def get_all_posts():
    mapper = 'posts'
    all_posts = Posts.query.all()
    return render_template("dashboard.html", category=mapper, get_all_post= all_posts, is_post_update = is_post_updating, user=current_user)

@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method =='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = Posts(title=title, content=content, author_id = current_user.id )
        note_db.session.add(new_post)
        note_db.session.commit()

    return redirect(url_for('posts.get_all_posts'))

@posts.route('/get-detail/<int:id>/changed-status', methods=['POST'])
@login_required
def change_status(id):

    if request.method == 'POST':
        state = request.form.get('status')
        get_post = Posts.query.filter_by(post_id = id).first_or_404()
        get_post.status = state
        note_db.session.commit()
    return redirect(url_for('posts.get_all_posts'))

@posts.route('/get-detail-of-post/<int:id>/see-more')
@login_required
def get_detail_post(id):
    get_post = Posts.query.filter_by(post_id = id).first_or_404()
    mapper = "status"
    return render_template("dashboard.html", category=mapper, status_post= get_post, is_post_update = is_post_updating, user=current_user)

@posts.route('/get-post-detail/<int:id>/<int:word>')
def get_post_detail(id, word):
    get_post = Posts.query.filter_by(post_id = id).first_or_404()
    author = User.query.filter_by(id = get_post.author_id).first_or_404()
    element_post = {}
    element_post['name'] = author.first_name + ' ' + author.last_name
    element_post['data'] = get_post
    return render_template("/blogs/home.html",is_on_detail = True, status_post = element_post, user=current_user)