"""Application configuration loaded from environment variables."""

import os


class Config:
    """Application configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'thermique_secret_key_2026')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'thermique_db')

    @property
    def DB_CONFIG(self):
        """Database configuration dictionary."""
        return {
            'host': self.DB_HOST,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'database': self.DB_NAME,
            'charset': 'utf8mb4',
        }
