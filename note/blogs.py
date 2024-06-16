from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import  current_user, login_required

from .models import Posts, User,Comments,Likes
from . import note_db


blogs = Blueprint('blogs',__name__)
on_detail = False

# home 
@blogs.route('/')
def home(count=3):
    post_data = []
    all_approved_posts = Posts.query.filter_by(status = 'approved').limit(count).all()
    for data in all_approved_posts:    
        author = User.query.filter_by(id=data.author_id).first_or_404()
        post_data.append({'author':author.first_name + ' ' + author.last_name,'data':data})

    return render_template("/blogs/home.html",is_on_detail = on_detail, user=current_user, approved_posts = post_data)


#  creating a comment 
@blogs.route('/create-comment', methods=['POST','GET'])
@login_required
def post_comment():

    if request.method == 'POST':
        comment_content = request.form.get('comment')
        post_id = request.form.get('post_id')
        user_id = request.form.get('author_id')

        new_comment = Comments(comment = comment_content, post_id=post_id, author_id=user_id)

        note_db.session.add(new_comment)
        note_db.session.commit()
    return redirect(url_for("posts.get_post_detail", id=post_id, word=3456))

#  get all comments by post id
@blogs.route('/get-all-comments-by-post/<int:id>')
def get_comment_by_post(id):

    all_comments = Comments.query.filter_by(post_id = id).all()
 
    return all_comments

# get an author that comments on a post
def get_comment_author(id):
    author = User.query.filter_by(id=id).first_or_404()
    return author.first_name + ' ' + author.last_name

# create like on a post
@blogs.route('/likes/create-like', methods=['POST','GET'])
@login_required
def create_like():
    print('we are here')
    if request.method == 'POST':
        posted_id = request.form.get('post_id')
        user_id = request.form.get('user_id')
        get_like = Likes.query.filter_by(post_id = posted_id, author_id = user_id).first()
        print(get_like)
        if get_like:
            note_db.session.delete(get_like)
            note_db.session.commit()
        else:
            new_like = Likes(post_id = posted_id, author_id = user_id)
            note_db.session.add(new_like)
            note_db.session.commit()
    return redirect(url_for("posts.get_post_detail", id=posted_id, word=348886))


