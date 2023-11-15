# main.py

import customtkinter as ctk
import os
import sqlite3
from login import Login
from register import Register
from storage import Storage

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("orange")

class MainApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.setup_database()

        self.title("Password Manager")
        self.geometry("960x540")
        self.resizable(False, False)

        container = ctk.CTkFrame(self)
        container.grid()

        # Create a dictionary with class references
        class_references = {
            "Login": Login,
            "Register": Register,
            "Storage": Storage,
        }

        self.frames = {}
        for window_name, window_class in class_references.items():
            frame = window_class(container, self)
            self.frames[window_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("Login")


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def setup_database(self):
        """
        Set up the SQLite database for user registration.

        This method:
        - checks if the database file already exists
        - creates a database folder if it doesn't exist
        - establishes a connection to the SQLite database file "AccessControlDB.db"
        - creates the "Users" table if it doesn't already exist.

        The "Users" table is designed to store user information for registration:
        - id INTEGER PRIMARY KEY AUTOINCREMENT,
        - username VARCHAR(256) NOT NULL
        - password VARCHAR(256) NOT NULL
        - encryption_key BLOB
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        # Check if the database file already exists
        if not os.path.exists(self.db_path):
            with sqlite3.connect(self.db_path) as connection:
                self.connect = connection
                self.cursor = connection.cursor()

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(256) NOT NULL,
                        password VARCHAR(256) NOT NULL,
                        encryption_key BLOB
                    )
                """)

            connection.close()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
