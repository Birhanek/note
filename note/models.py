# External imports
from flask_login import UserMixin
from sqlalchemy.sql import func

# Internal imports 
from . import note_db

# User information skeleton
class User(note_db.Model, UserMixin):
    
    id = note_db.Column(note_db.Integer, primary_key = True)
    email = note_db.Column(note_db.String(150), unique = True)
    password = note_db.Column(note_db.String(200))
    first_name = note_db.Column(note_db.String(100))
    last_name = note_db.Column(note_db.String(100))
    is_admin = note_db.Column(note_db.Boolean, default = False)
    notes = note_db.relationship('Note')
    posts = note_db.relationship('Posts')



# Note information skeleton
class Note(note_db.Model):
    id = note_db.Column(note_db.Integer, primary_key = True)
    title = note_db.Column(note_db.String(300))
    description = note_db.Column(note_db.String(1000))
    date = note_db.Column(note_db.DateTime(timezone=True), default=func.now())
    user_id = note_db.Column(note_db.Integer, note_db.ForeignKey('user.id'))

# Posts information skeleton
class Posts(note_db.Model):
    post_id = note_db.Column(note_db.Integer, primary_key=True)
    title = note_db.Column(note_db.String(100), nullable = False)
    content = note_db.Column(note_db.Text, nullable = False)
    publish_date = note_db.Column(note_db.DateTime(timezone=True), default=func.now())
    status = note_db.Column(note_db.String(50), nullable = False, default="pending")
    author_id = note_db.Column(note_db.Integer, note_db.ForeignKey('user.id'))

class Comments(note_db.Model):
    comment_id = note_db.Column(note_db.Integer,autoincrement=True, primary_key=True)
    comment = note_db.Column(note_db.Text, nullable=False)
    time_stamp = note_db.Column(note_db.DateTime(timezone=True), default=func.now())
    post_id = note_db.Column(note_db.Integer, note_db.ForeignKey('posts.post_id'))
    author_id = note_db.Column(note_db.Integer, note_db.ForeignKey('user.id'))

# Categories information skeleton
class Categories(note_db.Model):
    category_id = note_db.Column(note_db.Integer,autoincrement=True, primary_key=True)
    category_name = note_db.Column(note_db.String(200), nullable = False)
    category_description = note_db.Column(note_db.String(500))

# Post Categories information skeleton
class Post_categories(note_db.Model):
    post_id = note_db.Column(note_db.Integer, note_db.ForeignKey('posts.post_id'), primary_key=True)
    category_id = note_db.Column(note_db.Integer, note_db.ForeignKey('categories.category_id'), primary_key=True)

# Like information skeleton

class Likes(note_db.Model):
    like_id = note_db.Column(note_db.Integer, primary_key=True)
    time_stamp = note_db.Column(note_db.DateTime(timezone=True), default=func.now())
    post_id = note_db.Column(note_db.Integer, note_db.ForeignKey('posts.post_id'))
    author_id = note_db.Column(note_db.Integer, note_db.ForeignKey('user.id'))