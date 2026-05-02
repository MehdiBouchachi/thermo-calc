#!/usr/bin/env python
# thermocalc/scripts/setup_db.py
"""
Database initialization script for ThermoCalc.
Executes database.sql to create schema and seed reference data.
Reads database credentials from environment variables.
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Config

def setup_database():
    """
    Initialize database schema and reference data.
    
    Reads database.sql and executes all statements.
    Uses credentials from Config (env variables or defaults).
    """
    config = Config()
    
    try:
        print("Connecting to MySQL server...")
        conn = mysql.connector.connect(**config.DB_CONFIG)
        cursor = conn.cursor()
        
        # Read and execute the SQL file
        db_script = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'database.sql'
        )
        print(f"Reading database script from {db_script}...")
        with open(db_script, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolon and execute each statement
        for statement in sql_content.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print('✓ Database setup completed successfully!')
        cursor.close()
        conn.close()
    except Error as e:
        print(f'✗ Error: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'✗ Unexpected error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    setup_database()
