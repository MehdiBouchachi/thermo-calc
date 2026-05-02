# thermocalc/app/__init__.py
"""
Flask application factory module.
Creates and configures the Flask application with all necessary settings and blueprints.
"""

from flask import Flask
from app.config import get_config
from app.routes import register_blueprints


def create_app(config=None):
    """
    Application factory function.
    
    Creates and configures a Flask application instance with:
    - Configuration management
    - Blueprint registration
    - Error handlers
    
    Args:
        config: Config object or config name string.
               If None, uses environment or defaults to development.
    
    Returns:
        Configured Flask application instance.
    """
    
    # Get configuration
    if config is None:
        config = get_config()
    elif isinstance(config, str):
        config = get_config(config)
    
    # Create Flask app with explicit template and static folders
    # Templates and static files are in the project root, not the app package
    import os
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(__name__, 
                template_folder=os.path.join(root_path, 'templates'),
                static_folder=os.path.join(root_path, 'static'))
    
    # Configure app
    app.secret_key = config.SECRET_KEY
    app.debug = config.DEBUG
    
    # Register blueprints
    register_blueprints(app)
    
    return app
