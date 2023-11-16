"""
Register Module

This module defines the Register class, which represents the registration form
for user accounts. It utilizes the customtkinter library for GUI components
and integrates with SQLite for user data storage. User passwords are hashed
using the bcrypt library for security.

Classes:
    Register: A customtkinter frame for user registration.

Note:
    The module assumes the existence of the customtkinter library,
    the login module, and the sidebar module for proper functioning.
    It also requires the bcrypt library for password hashing.
"""

import os
import sqlite3
import customtkinter as ctk
import bcrypt
from sidebar import SideBarFrame

class Register(ctk.CTkFrame):
    """
    Register Class

    This class represents the user registration form, utilizing the customtkinter library
    for GUI components. It includes entry fields for the username and password, with an option
    to display the password using a checkbox.
    The registration process is handled through the "Register" button,
    and users can navigate back to the login form using the "Back To Login" button.

    Attributes:
        - username (ctk.CTkEntry): Entry field for the username.
        - password (ctk.CTkEntry): Entry field for the password.
        - repeat_password (ctk.CTkEntry): Entry field for repeating the password.
        - checkbox (ctk.CTkCheckBox): Checkbox for toggling password visibility.
        - button_register (ctk.CTkButton): Button for initiating the registration process.
        - error_label (ctk.CTkLabel): Label for displaying error messages during registration.

    Methods:
        - __init__: Initializes the Register class, setting up the form and components.
        - setup_database: Set up the SQLite database for user registration.
        - button_register_event: Handles the registration process.
        - reveal_password: Toggles the visibility of password.
    """
    def __init__(self, parent, controller, user_id):
        ctk.CTkFrame.__init__(self, parent)


        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        sidebar.label("Register Form")
        self.cursor = None

        self.back_to_login = ctk.CTkButton(sidebar.frame, text="Back To Login",
                                           command=lambda: controller.show_frame("Login"))
        self.back_to_login.grid(row=2, column=0, padx=20, pady=10)

        # create register form
        self.register_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.register_form_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsw")
        self.register_form_frame.grid_columnconfigure(0, weight=0)
        self.register_form_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        self.username = ctk.CTkEntry(master=self.register_form_frame,
                                     placeholder_text="Username")
        self.username.grid(row=0, column=0, pady=12, padx=80, sticky="ew")

        self.password = ctk.CTkEntry(master=self.register_form_frame,
                                     placeholder_text="Password", show="*")
        self.password.grid(row=1, column=0, pady=12, padx=80, sticky="ew")

        self.repeat_password = ctk.CTkEntry(master=self.register_form_frame,
                                            placeholder_text="Repeat Password", show="*")
        self.repeat_password.grid(row=2, column=0, pady=12, padx=80, sticky="ew")

        self.checkbox_var = ctk.StringVar(value="off")  # Initialize checkbox value as "off"
        self.checkbox = ctk.CTkCheckBox(master=self.register_form_frame, text="Show Password",
                                        command=self.reveal_password, variable=self.checkbox_var,
                                        onvalue="on", offvalue="off")
        self.checkbox.grid(row=3, column=0, pady=0, padx=80, sticky="ew")

        self.button_register = ctk.CTkButton(master=self.register_form_frame, text="Register",
                                              command=self.button_register_event)
        self.button_register.grid(row=4, column=0, pady=6, padx=120, sticky="ew")

        self.error_label = ctk.CTkLabel(self.register_form_frame, text="", fg_color="transparent")
        self.error_label.grid(row=5, column=0, padx=80, sticky="ew")


    def button_register_event(self):
        """
        Handles the registration process when the "Register" button is clicked.

        - Retrieves the entered username and passwords
        - validates the inputs
        - checks for existing usernames
        - registers a new user if the inputs are valid and the username is not already taken.

        Raises:
            Exception: An error occurred during the registration process.

        Note:
            - This method assumes the existence of the "Users" table in the database.
            - Passwords are hashed using bcrypt before being stored in the database.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        # Check if the database file already exists

        with sqlite3.connect(self.db_path) as connection:
            self.connect = connection
            self.cursor = connection.cursor()

        username = self.username.get()
        password = self.password.get()
        repeat_password = self.repeat_password.get()

        # User input handling
        try:
            if not username or not password or not repeat_password:
                self.error_label.configure(text="Please fill in all fields", fg_color="red")
                return

            if password != repeat_password:
                self.error_label.configure(text="Passwords do not match", fg_color="red")
                return

            # Register User
            self.cursor.execute("SELECT username FROM Users WHERE username=?", [username])
            if self.cursor.fetchone() is not None:
                self.error_label.configure(text="Username already exists", fg_color="red")
                return

            else:
                encoded_password = password.encode("utf-8")
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                self.cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                                    [username, hashed_password])

                self.connect.commit()
                self.error_label.configure(text="Account has been created", fg_color="green")

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            self.error_label.configure(text="An error occurred during registration.",
                                       fg_color="red")

    def reveal_password(self):
        """
        Toggles the visibility of password entries based on the state of a checkbox.

        - If the checkbox is checked ("on"), the password entries are displayed as plain text.
        - If the checkbox is unchecked ("off"), the password entries are displayed as * for security

        Note:
            - This method is bound to a checkbox's command to dynamically update password visibility
        """
        show_text = self.checkbox_var.get() == "on"
        if show_text:
            self.password.configure(show="")
            self.repeat_password.configure(show="")
        else:
            self.password.configure(show="*")
            self.repeat_password.configure(show="*")
