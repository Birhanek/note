from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import  current_user, login_required

from .models import Note
from . import note_db


blogs = Blueprint('blogs',__name__)

@blogs.route('/')
def home():
    return render_template("/blogs/home.html", user=current_user)