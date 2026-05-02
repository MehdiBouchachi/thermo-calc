#!/usr/bin/env python
"""Setup database script for ThermoCalc"""

import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'life3002%%IdHeM',
}

try:
    print("Connecting to MySQL server...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Read and execute the SQL file
    print("Reading database.sql...")
    with open('database.sql', 'r', encoding='utf-8') as f:
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
    exit(1)
except Exception as e:
    print(f'✗ Unexpected error: {e}')
    exit(1)
