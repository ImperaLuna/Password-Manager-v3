"""
Password Manager Application

This module implements the main functionality of a Password Manager application using
customtkinter for the graphical user interface and SQLite for database storage.

Classes:
    - MainApp: The main application class that initializes the GUI,
    manages frames for different windows (Login, Register, Storage),
    and sets up the SQLite database for user registration.

Usage:
    Run this module to launch the Password Manager application.
    The application provides features for user login, registration, and storage of passwords.
"""

import customtkinter as ctk
import os
import sqlite3
from login import Login
from register import Register
from storage import Storage

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("orange")

class MainApp(ctk.CTk):
    """
    Main application class for the Password Manager.

    This class initializes the GUI for the Password Manager application:
    - including the main window title, size, and configuration
    - it sets up the SQLite database
    - creates instances of frames for login, registration, and storage
    - displays the initial "Login" frame.

    Attributes:
        - frames (dict): A dictionary to store instances of different frames
            for switching between windows.

    Methods:
        show_frame: Displays the specified frame within the Tkinter application.
        setup_database: Sets up the SQLite database for user registration.

    Usage:
        Create an instance of this class to run the Password Manager application.
    """
    def __init__(self):
        ctk.CTk.__init__(self)
        self.setup_database()

        self.title("Password Manager")
        self.geometry("960x540")
        self.resizable(False, False)

        container = ctk.CTkFrame(self)
        container.grid()

        class_references = {
            "Login": Login,
            "Register": Register,
            "Storage": Storage,
        }

        user_id = 0
        self.frames = {}
        for window_name, window_class in class_references.items():
            frame = window_class(container, self, user_id)
            self.frames[window_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("Login")

    def show_frame(self, window):
        """
        Display the specified frame within the application.

        Parameters:
            window (str): The name of the frame to be displayed, such as
              "Login," "Register," or "Storage."

        Behavior:
            - If switching to the "Storage" frame, pass the user_id
                to generate user data buttons inside the scrollable frame.
            - Calls the `set_user_id` method on the target frame to set the user_id.
            - Calls the `create_account_buttons` method on the "Storage" frame
                to generate account buttons.
            - Raises the specified frame to the front.

        Args:
            - window (str): The name of the frame to be displayed.
        """
        frame = self.frames[window]

        # If switching to the Storage frame, pass the user_id in order to
        #  generate the user data buttons inside the scrollable frame
        if window == "Storage":
            user_id = self.frames["Login"].get_user_id()
            frame.set_user_id(user_id)
            self.frames["Storage"].create_account_buttons()

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
