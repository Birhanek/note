# External imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required

# internal imports
from .models import Posts, User,Likes
from . import note_db
from .blogs import get_comment_by_post, get_comment_author

posts = Blueprint('posts', __name__)

# this controls are we updating or creating a post
is_post_updating = False

# this controls the expanding or collapsing of post
is_collapsed = True

# fetching all posts
@posts.route('/')
@login_required
def get_all_posts():
    mapper = 'posts'
    all_posts = Posts.query.all()
    
    return render_template("dashboard.html", 
                           category=mapper, 
                           get_all_post= all_posts, 
                           is_post_update = is_post_updating, 
                           user=current_user,
                           is_expanding = is_collapsed)

# Creating a post
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

# Changing the status of a post that is managed by the administrator 
@posts.route('/get-detail/<int:id>/changed-status', methods=['POST'])
@login_required
def change_status(id):

    if request.method == 'POST':
        state = request.form.get('status')
        get_post = Posts.query.filter_by(post_id = id).first_or_404()
        get_post.status = state
        note_db.session.commit()
    return redirect(url_for('posts.get_all_posts'))

#  get the details of a post
@posts.route('/get-detail-of-post/<int:id>/see-more')
@login_required
def get_detail_post(id):
    get_post = Posts.query.filter_by(post_id = id).first_or_404()
    mapper = "status"
    return render_template("dashboard.html", category=mapper, 
                           status_post= get_post, 
                           is_post_update = is_post_updating, 
                           user=current_user)

# post detail and a writer or an author
@posts.route('/get-post-detail/<int:id>/<int:word>')
def get_post_detail(id, word):

    get_post = Posts.query.filter_by(post_id = id).first_or_404()
    author = User.query.filter_by(id = get_post.author_id).first_or_404()
    total_like = Likes.query.filter_by(post_id = id).all()
    all_comment_by_post = get_comment_by_post(id)
     
    comment_data_collector = []
    #  iterate over the comments given for the post to classify 
    #  the replier and what s/he commented
    for comment in all_comment_by_post:
        comment_author = get_comment_author(comment.author_id)
        comment_collector = {
             'author': comment_author,
             'comment': comment
         }
        comment_data_collector.append(comment_collector)

    element_post = {}
    element_post['name'] = author.first_name + ' ' + author.last_name
    element_post['data'] = get_post
    print(element_post)
    return render_template("/blogs/home.html",
                           is_on_detail = True, 
                           status_post = element_post, 
                           all_comments = comment_data_collector,
                           total_likes = len(total_like),
                           user=current_user)

# delete a post
@posts.route('/get-delete-post/<int:id>/<int:extra>')
@login_required
def delete_post_by_id(id, extra):
    deleted_post = Posts.query.filter_by(post_id = id).first_or_404()

    note_db.session.delete(deleted_post)
    note_db.session.commit()

    return redirect(url_for('posts.get_all_posts'))


# Get the post before you update a post
@posts.route('/get-post-for-update/<int:id>/edit')
@login_required
def get_post_by_id_to_update(id):
    get_post = Posts.query.filter_by(post_id = id).first_or_404()
    mapper = 'posts'
    print(get_post.content)
    is_post_updating = True

    return render_template("dashboard.html",
                           category=mapper, 
                           set_post= get_post, 
                           is_post_update = is_post_updating, 
                           user=current_user)

# Update a post
@posts.route('/update-<int:longer_id>/<int:id>/updating', methods=['POST'])
@login_required
def update_post(longer_id : int, id: int) -> str:
    global is_post_updating
    get_post = Posts.query.filter_by(post_id = id).first_or_404()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        get_post.title = title
        get_post.content = content
        note_db.session.commit()
    is_post_updating = False
    
    return redirect(url_for('posts.get_all_posts'))

# searching a blog
@posts.route('/searching')
def searching_post():
    searching_word = request.form.get('search')
    
