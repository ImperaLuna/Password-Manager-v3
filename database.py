"""
database.py

This module defines a Database class for managing SQLite databases. It includes methods for setting up the database,
managing connections within a context, and logging relevant information.

Classes:
    - DataBase: Represents a SQLite database and provides methods for database management.

Module Constants:
    - LOGGING_PATH: Path to the log file for recording events.
    - DATABASE_NAME: The name of the database.
    - DATABASE_FOLDER: The folder path where the database file is stored.
    - DATABASE_PATH: The full path to the database file.

Dependencies:
    - sqlite3
    - logging
    - pathlib
    - constants (imported as const)
"""
import sqlite3
import logging
from pathlib import Path
import constants as const

logging.basicConfig(level=logging.INFO, filename=const.LOGGING_PATH,
                    format="%(asctime)s -  %(levelname)s - Module: %(module)s - %(message)s")
logger = logging.getLogger(__name__)

class DataBase:
    """
    A class representing a SQLite database.

    Attributes:
        name (str): The name of the database.
        folder (str): The folder path where the database file is stored.
        path (str): The full path to the database file.

    Methods:
        __init__(): Initializes the DataBase object.
        __enter__(): Enters a context to manage the database connection.
        __exit__(): Exits the context and commits changes to the database.
        setup_database(): Sets up the database by creating folders and tables if they do not exist.
    """
    def __init__(self):
        """
        Initializes a new instance of the DataBase class.
        """
        self.name = const.DATABASE_NAME
        self.folder = const.DATABASE_FOLDER
        self.path = const.DATABASE_PATH

    def __enter__(self):
        """
        Enters a context to manage the database connection.

        Returns:
            DataBase: The current instance of the DataBase class.
        """
        self.setup_database()
        self.connection = sqlite3.connect(self.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context and commits changes to the database.
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def setup_database(self):
        """
        Sets up the database by creating folders and tables if they do not exist.
        """
        try:
            if not Path(self.folder).is_dir():
                Path(self.folder).mkdir()
                logger.info(f"Created folder with path: {self.folder}")
        except Exception as e:
            logger.error(f"An error occurred while setting up the folder: {e}")

        try:
            if not Path(self.path).is_file():
                Path(self.path).touch()
                logger.info(f"Created database file at address: {self.path}")

                with sqlite3.connect(self.path) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username VARCHAR(256) NOT NULL,
                            password VARCHAR(256) NOT NULL,
                            encryption_key BLOB
                        )
                    """)
                logger.info(f"Table Users was created inside: {self.name} at address {self.path}")
        except Exception as e:
            logger.error(f"An error occurred while setting up the database: {e}")

    def register_check_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT username FROM Users WHERE username=?", (username,))

        if cursor.fetchone() is not None:
            user_exists = True
        else:
            user_exists = False
        return user_exists
    
    def register_user(self, username, hashed_password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                                    (username, hashed_password))
        
    def login_check(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ID, Password FROM Users WHERE Username=?", (username,))
        result = cursor.fetchone()
        return result

    def login_retrieve_encryption_key(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT encryption_key FROM Users WHERE Username=?", (username,))
        db_encryption_key = cursor.fetchone()
        encryption_key = db_encryption_key[0]
        return encryption_key

    def login_save_encryption_key(self, encryption_key, username):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Users SET Encryption_key=? WHERE Username=?",
                        (encryption_key, username))
        
    def generator_save_user_data(self, values):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO UserData (entry_name, entry_username, entry_password, entry_website, User_id)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, values)

    def storage_create_account_buttons(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="UserData"')
        table_exists = cursor.fetchone()

        if not table_exists:
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
        cursor.execute("SELECT entry_name FROM UserData WHERE User_id=?", [user_id])
        account_names = cursor.fetchall()
        return account_names


    def storage_fetch_user_data(self, account_name, user_id):
        cursor = self.connection.cursor()
        query = (
            "SELECT entry_id, entry_name, entry_username, entry_password, entry_website "
            "FROM UserData WHERE entry_name=? AND User_id=?"
        )
        data = (account_name, user_id)
        cursor.execute(query, data)
        account_details = cursor.fetchone()
        return account_details

    def storage_get_id_for_update(self, current_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT entry_id FROM UserData WHERE entry_id=?", (current_id,))
        result = cursor.fetchone()
        return result

    def storage_update_user_data(self, data):
        cursor = self.connection.cursor()

        query = (
            "UPDATE UserData SET entry_name=?, entry_username=?, "
            "entry_password=?, entry_website=? WHERE entry_id=?"
        )
        
        cursor.execute(query, data)

    def storage_fetch_details(self, account_index):
        cursor = self.connection.cursor()
        query = (
            "SELECT entry_name, entry_username, entry_password, entry_website "
            "FROM UserData LIMIT 1 OFFSET ?"
        )
        data = (account_index,)
        cursor.execute(query, data)
        account_details = cursor.fetchone()
        return account_details
    
    def storage_delete_details(self, entry_id):
        print(f"Deleting entry with entry_id: {entry_id}")
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM UserData WHERE entry_id = ?", (entry_id,))


