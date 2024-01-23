"""
Login Module

This module defines the Login class, which represents the logic behind user authentication.
It utilizes the customtkinter library for GUI components
and integrates with SQLite for user data storage.


Classes:
    Login: A customtkinter frame for Login logic.
"""


import bcrypt
import customtkinter as ctk
from sidebar import SideBarFrame
import json
import logging
from cryptography.fernet import Fernet
from database import DataBase
import constants as const


logging.basicConfig(level=logging.INFO, filename=const.LOGGING_PATH,
                    format="%(asctime)s - Module: %(levelname)s - %(module)s - %(message)s")
logger = logging.getLogger(__name__)

class Login(ctk.CTkFrame):
    """
    The Login class represents a customtkinter frame designed for user authentication.

    This class handles user login functionality, including interactions with the GUI
    components provided by the customtkinter library and data storage in SQLite.

    Attributes:
        user_id (int): The user ID associated with the authenticated user.

    Methods:
        - login(self, controller, storage_class):
            Handles the login process, validates user credentials, and navigates to the
            specified storage frame upon successful authentication.

        - save_credentials(self, username, password):
            Encrypts and saves user credentials, including the username and password,
            to a JSON file for future use.

        - check_credentials_file(self):
            Checks for the existence of a credentials file, retrieves stored credentials,
            and populates the username and password fields if found.

        - delete_credentials(self):
            Deletes the stored credentials file, removing any saved login information.

        - clear_login(self):
            Clears the login fields, such as username and password, based on the state
            of the "Remember Me" checkbox.

        - save_user_id(self, user_id):
            Sets the user_id attribute with the provided user ID.

        - get_user_id(self):
            Retrieves the user ID associated with the authenticated user.
"""
    def __init__(self, parent, controller, user_id):
        ctk.CTkFrame.__init__(self, parent)

        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        sidebar.label("Login")

        self.user_id = None
        
        self.login_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.login_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsw")
        self.login_frame.grid_columnconfigure(0, weight=0)
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        self.username_entry = ctk.CTkEntry(master=self.login_frame,
                                        placeholder_text="Username")
        self.username_entry.grid(row=0, column=0, pady=12, padx=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(master=self.login_frame,
                                        placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=0, pady=12, padx=10, sticky="ew")

        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(master=self.login_frame,
                                        text="Remember Me", variable=self.checkbox_var)
        self.checkbox.grid(row=2, column=0, pady=6, padx=50, sticky="ew")
        self.check_credentials_file()

        self.login_button = ctk.CTkButton(master=self.login_frame, text="Login",
                                command=lambda: self.login(controller, "Storage"))
        self.login_button.grid(row=3, column=0, pady=6, padx=50, sticky="ew")

        self.register_button = ctk.CTkButton(master=self.login_frame, text="Register",
                                command=lambda: controller.show_frame("Register"))
        self.register_button.grid(row=5, column=0, pady=6, padx=50, sticky="ew")

        self.verification_label = ctk.CTkLabel(self.login_frame, text="",
                                         fg_color="transparent")
        self.verification_label.grid(row=6, column=0, padx=12, sticky="ew")


    def login(self, controller, storage_class):
        """
        Handles user authentication.

        Parameters:
        - controller: An instance of the application controller used for frame switching.
        - storage_class: The class representing the storage frame in the application.
        """

        checkbox_execute = self.checkbox_var.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            if not username or not password:
                self.verification_label.configure(text="Please enter username and password",
                                            fg_color="red")
                return

            with DataBase() as db: 
                result = db.login_check(username)
            if result:
                user_id, hashed_password = result
                if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                    self.save_user_id(user_id)
                    controller.show_frame(storage_class)

                    # Save credentials if the "Remember Me" checkbox is checked
                    if checkbox_execute:
                        self.save_credentials(username, password)
                    else:
                        self.delete_credentials()
                        self.clear_login()
                else:
                    self.verification_label.configure(text="Invalid password", fg_color="red")
            else:
                self.verification_label.configure(text="Invalid username", fg_color="red")
        except Exception as e:
            self.verification_label.configure(text="An error occurred during registration.", fg_color="red")
            logger.error(f"An error occurred while setting up the database: {e}")

    def save_credentials(self, username, password):
        """
        Saves the user's credentials (username and password) in a JSON file.
        Encrypts the password using they key from the database or generates
        a new one if it doesn't exist

        Parameters:
        - username: The username to be saved.
        - password: The password to be saved.
        """
        with DataBase() as db:
            encryption_key = db.login_retrieve_encryption_key(username)

        if not encryption_key:
            encryption_key = Fernet.generate_key()

            with DataBase() as db:
                db.login_save_encryption_key(encryption_key, username)

        fernet = Fernet(encryption_key)
        encrypted_password = fernet.encrypt(password.encode("utf-8")).decode("utf-8")


        credentials = {"username": username, "password": encrypted_password}
        
        const.CREDENTIALS_FOLDER.mkdir(exist_ok=True)
        with open(const.CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(credentials, f)

    def check_credentials_file(self):
        """
        Checks if there is a stored credentials file. If found, reads the credentials,
        decrypts the password, and populates the username and password entry fields accordingly.
        Also sets the "Remember Me" checkbox if credentials are loaded successfully.
        """


        try:

            with open(const.CREDENTIALS_PATH, "r", encoding="utf-8") as f:
                credentials = json.load(f)
                username, encrypted_password = (credentials.get("username", ""),
                                                credentials.get("password", ""))

                with DataBase() as db:
                    encryption_key = db.login_retrieve_encryption_key(username)

                fernet = Fernet(encryption_key)
                password = fernet.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")

                self.username_entry.insert(ctk.END, username)
                self.password_entry.insert(ctk.END, password)

                self.checkbox_var.set(True)

        except FileNotFoundError:
            self.checkbox_var.set(False)

    def delete_credentials(self):
        """
        Deletes the stored credentials file if it exists.
        """
        try:
            const.CREDENTIALS_PATH.unlink()
            const.CREDENTIALS_FOLDER.rmdir()
        except FileNotFoundError:
            pass

    def clear_login(self):
        """
        Clears the username and password entry fields if the "Remember Me" checkbox is not checked.
        """
        checkbox_execute = self.checkbox_var.get()

        if not checkbox_execute:
            self.username_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)

    def save_user_id(self, user_id):
        """
        Saves the user ID obtained during the login process.

        Parameters:
        - user_id: The ID of the authenticated user.
        """
        self.user_id = user_id

    def get_user_id(self):
        """
        Returns:
        - The user ID of the authenticated user.
        """
        return self.user_id

