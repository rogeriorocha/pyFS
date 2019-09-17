from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask("fs", instance_relative_config=False)
    
    #app.config.from_object('config.Config')
    
    # Remover
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "super secret key"

    #db.app = app
    db.init_app(app)

    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app