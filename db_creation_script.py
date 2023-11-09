import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('db_test.db')
cursor = conn.cursor()

# Create the "accounts" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT,
        password TEXT,
        website TEXT
    )
''')

# Insert 5 accounts into the database
accounts = [
    ("Jane", "jane", "password1234", "amazon.com"),
    ("John", "john", "securepwd456", "google.com"),
    ("Alice", "alice", "mysecret123", "facebook.com"),
    ("Bob", "bob", "bobspass", "twitter.com"),
    ("Eve", "eve", "eve123", "linkedin.com")
]

cursor.executemany('INSERT INTO accounts (name, username, password, website) VALUES (?, ?, ?, ?)', accounts)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Database 'db_test.db' created and populated with 5 accounts.")
