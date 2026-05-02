# thermocalc/app/routes/__init__.py
"""
Route registration module.
Imports and registers all blueprints with the Flask application.
"""

from flask import Blueprint
from app.routes import batiments, api, stats


def register_blueprints(app):
    """
    Register all application blueprints.
    
    Args:
        app: Flask application instance.
    """
    app.register_blueprint(batiments.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(stats.bp)
