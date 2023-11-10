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
    ("Netflix", "JaneDoe123", "password1234", "netflix.com"),
    ("Spotify", "JAmazonUser", "securepwd456", "spotify.com"),
    ("Github", "AmazonJane", "mysecret123", "github.com"),
    ("Instagram", "JanetheGreat", "bobspass", "instagram.com"),
    ("Stackoverflow", "J123ane", "eve123", "stackoverflow.com"),
    ("Microsoft", "Janerocks456", "password1234", "microsoft.com"),
    ("Reddit", "Jane_Online", "securepwd456", "reddit.com"),
    ("Youtube", "J123ane", "mysecret123", "youtube.com"),
    ("Apple", "AmazonQueen", "bobspass", "apple.com"),
    ("Dropbox", "JaneLovesShopping", "eve123", "dropbox.com"),
    ("Ebay", "JanetheGreat", "password1234", "ebay.com"),
    ("Pinterest", "JanesWorld789", "securepwd456", "pinterest.com"),
    ("Twitch", "AmazonJaneD", "mysecret123", "twitch.tv"),
    ("Hulu", "JaneOnline123", "bobspass", "hulu.com"),
    ("Wordpress", "J_Shopper", "eve123", "wordpress.com")
]




cursor.executemany('INSERT INTO accounts (name, username, password, website) VALUES (?, ?, ?, ?)', accounts)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Database 'db_test.db' created and populated with 5 accounts.")
