import sqlite3
from app.databases.tables import tables_definition

# Database configuration for development environment
DB_FILE = 'development.db'


def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create tables if they don't exist
    for table_name, table_definition in tables_definition.items():
        cursor.execute(table_definition)

    # Commit changes and close connection
    conn.commit()
    conn.close()


def get_connection():
    # Return connection to the SQLite database
    return sqlite3.connect(DB_FILE)
