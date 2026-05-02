"""Database connection utilities."""

from mysql.connector import connect, Error
from flask import current_app


def get_connection():
    """Open and return a MySQL connection using app config. Returns None on failure."""
    try:
        cfg = current_app.config
        return connect(
            host=cfg['DB_HOST'],
            user=cfg['DB_USER'],
            password=cfg['DB_PASSWORD'],
            database=cfg['DB_NAME'],
            charset='utf8mb4'
        )
    except Error as e:
        current_app.logger.error('DB connection failed: %s', e)
        return None


def get_cursor(conn):
    """Returns a dictionary cursor."""
    return conn.cursor(dictionary=True)
