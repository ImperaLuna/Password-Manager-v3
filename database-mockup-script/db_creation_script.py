import sqlite3
import string
import random
import bcrypt

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def hash_password(password):
    encoded_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password

def create_and_populate_database():
    conn = sqlite3.connect('AccessControlDB.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(256) NOT NULL,
            password BLOB NOT NULL,
            encryption_key BLOB
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserData (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_name VARCHAR(256),
            entry_username VARCHAR(256),
            entry_password VARCHAR(256),
            entry_website VARCHAR(256),
            User_id INTEGER,
            FOREIGN KEY (User_id) REFERENCES Users(id)
        )
    ''')

    usernames = ['TestUser1', 'TestUser2', 'TestUser3', 'TestUser4', 'TestUser5']
    password = 'test'
    accounts = [
        ("Netflix", generate_random_string(8), generate_random_string(12), "netflix.com"),
        ("Spotify", generate_random_string(8), generate_random_string(12), "spotify.com"),
        ("Github", generate_random_string(8), generate_random_string(12), "github.com"),
        ("Instagram", generate_random_string(8), generate_random_string(12), "instagram.com"),
        ("Stackoverflow", generate_random_string(8), generate_random_string(12), "stackoverflow.com"),
        ("Microsoft", generate_random_string(8), generate_random_string(12), "microsoft.com"),
        ("Reddit", generate_random_string(8), generate_random_string(12), "reddit.com"),
        ("Youtube", generate_random_string(8), generate_random_string(12), "youtube.com"),
        ("Apple", generate_random_string(8), generate_random_string(12), "apple.com"),
        ("Dropbox", generate_random_string(8), generate_random_string(12), "dropbox.com"),
        ("Ebay", generate_random_string(8), generate_random_string(12), "ebay.com"),
        ("Pinterest", generate_random_string(8), generate_random_string(12), "pinterest.com"),
        ("Twitch", generate_random_string(8), generate_random_string(12), "twitch.tv"),
        ("Hulu", generate_random_string(8), generate_random_string(12), "hulu.com"),
        ("Wordpress", generate_random_string(8), generate_random_string(12), "wordpress.com")
    ]

    for username in usernames:
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO Users (username, password, encryption_key)
            VALUES (?, ?, NULL)
        ''', (username, hashed_password))

        for user_id in range(1, 6):
            for _ in range(5):
                entry_name, entry_username, entry_password, entry_website = random.choice(accounts)
                entry_name = f'TestCase{user_id} - {entry_name}'
                cursor.execute('''
                    INSERT INTO UserData (entry_name, entry_username, entry_password, entry_website, User_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (entry_name, entry_username, entry_password, entry_website, user_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_and_populate_database()
    print('Sample data has been inserted into the AccessControlDB database.')
