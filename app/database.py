# thermocalc/app/database.py
"""
Database connection management for ThermoCalc.
Provides utilities to establish and manage MySQL connections.
"""

import mysql.connector
from mysql.connector import Error
from app.config import Config


def get_db_connection(config=None):
    """
    Establish and return a MySQL database connection.
    
    Args:
        config: Config object containing database credentials.
               If None, uses the default Config class.
    
    Returns:
        MySQL connection object, or None if connection fails.
    """
    if config is None:
        config = Config()
    
    try:
        conn = mysql.connector.connect(**config.DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def get_cursor(conn, dictionary=True):
    """
    Get a cursor from an active database connection.
    
    Args:
        conn: Active MySQL connection.
        dictionary: If True, return rows as dictionaries; else as tuples.
    
    Returns:
        Database cursor.
    """
    return conn.cursor(dictionary=dictionary)
