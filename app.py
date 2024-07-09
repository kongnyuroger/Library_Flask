from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()

def create_app():
    app =Flask(__name__,template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./librarydb.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB
    
    


    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    db.init_app(app)
    bcrypt = Bcrypt(app)
    from routes import register_routes
    register_routes(app, db, bcrypt,)
    migrates = Migrate(app, db, bcrypt,)
    return app