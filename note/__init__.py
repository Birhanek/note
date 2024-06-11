from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# initialize the SQLAlchemy database object to use it as a database
note_db = SQLAlchemy()

# define database name
DB_Name = "notes.db"

# create the application with all the initializations
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "HSGGDGjajajdkdgugd"

    #configure the database location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'

    note_db.init_app(app)

    from .views import views
    from .auth import auth
    from .profile import profile
    from .blogs import blogs
    from .category import category
    from .posts import posts
   

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/auth/')
    app.register_blueprint(profile, url_prefix ='/profile/')
    app.register_blueprint(blogs, url_prefix='/news/')
    app.register_blueprint(category, url_prefix = '/category/')
    app.register_blueprint(posts, url_prefix = '/posts/')
   
   

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('note/' + DB_Name):
        with app.app_context():
            note_db.create_all()
            
            print('Database created!')

    

