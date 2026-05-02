"""Flask application factory."""

from flask import Flask
from app.config import Config


def create_app(config_class=Config):
    """Application factory. Creates and configures the Flask app."""
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    
    cfg = config_class()
    app.secret_key = cfg.SECRET_KEY
    app.config['DB_HOST'] = cfg.DB_HOST
    app.config['DB_USER'] = cfg.DB_USER
    app.config['DB_PASSWORD'] = cfg.DB_PASSWORD
    app.config['DB_NAME'] = cfg.DB_NAME

    from app.routes import register_blueprints
    register_blueprints(app)

    return app
