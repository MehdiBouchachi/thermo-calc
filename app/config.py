# thermocalc/app/config.py
"""
Configuration management for ThermoCalc application.
Reads settings from environment variables with sensible defaults for development.
"""

import os


class Config:
    """
    Base configuration class.
    Loads settings from environment variables with defaults.
    """
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'thermique_secret_key_2026')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'life3002%%IdHeM'),
        'database': os.getenv('DB_NAME', 'thermique_db'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""
    ENV = 'production'
    DEBUG = False


class TestingConfig(Config):
    """Testing environment configuration."""
    ENV = 'testing'
    DEBUG = True
    TESTING = True


def get_config(config_name=None):
    """
    Get the appropriate configuration class.
    
    Args:
        config_name: Name of config ('development', 'production', 'testing').
                    If None, uses FLASK_ENV or defaults to 'development'.
    
    Returns:
        Config class instance.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return configs.get(config_name, DevelopmentConfig)()
