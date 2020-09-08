import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

# Create extension objects etc
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Access denied'

def create_app(config='config-postgres.py'):
    """
    Application factory

    config -- configuration file, default = config.py
    """
    db = SQLAlchemy()

    # import utils (e.g. login loader)
    import app.utils

    # create & configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    initialize_extensions(app)
    register_blueprints(app)

    return app

def initialize_extensions(app):
    """Link extensions to an app"""
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)

def register_blueprints(app):
    """Register blueprints to an app"""
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.idea import bp as idea_bp
    app.register_blueprint(idea_bp, url_prefix='/idea')

    from app.shorten import bp as shorten_bp
    app.register_blueprint(shorten_bp)
