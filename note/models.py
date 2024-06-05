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



# Note information skeleton
class Note(note_db.Model):
    id = note_db.Column(note_db.Integer, primary_key = True)
    title = note_db.Column(note_db.String(300))
    description = note_db.Column(note_db.String(1000))
    date = note_db.Column(note_db.DateTime(timezone=True), default=func.now())
    user_id = note_db.Column(note_db.Integer, note_db.ForeignKey('user.id'))

