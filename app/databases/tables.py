# Define database tables
tables_definition = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'financial_indicators': '''
        CREATE TABLE IF NOT EXISTS financial_indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            indicator_name TEXT,
            value REAL,
            currency TEXT,
            date DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''',
    'personal_finance': '''
        CREATE TABLE IF NOT EXISTS personal_finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_name TEXT,
            amount REAL,
            category TEXT,
            currency TEXT,
            date DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    '''
}
