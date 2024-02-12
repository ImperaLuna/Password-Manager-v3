"""
storage_module.py

This module defines the `Storage` class, which represents a component of a password
storage and management system implemented using the Tkinter library. It includes
features such as creating, updating, and displaying user account details, as well
as a password generator and a log-out option.

Classes:
    - Storage: A Tkinter frame that serves as the main interface for managing user accounts.

Usage:
    The `Storage` class is typically instantiated within a larger application,
    and it interacts with other modules and classes to provide a user-friendly
    interface for storing and managing passwords.

Dependencies:
    - customtkinter: A custom Tkinter library providing enhanced widgets.
    - os: Operating system-specific functionality.
    - sidebar: Module defining the SideBarFrame class for the sidebar interface.
    - generator: Module defining the Generator and EntryFrame classes.
    - sqlite3: SQLite database connectivity for storing user account information.
    - pyperclip: A cross-platform clipboard module for copying username and password.
    - webbrowser: A module providing a high-level interface to allow displaying
      web-based documents to users.

Note:
    Before using this module, ensure that the required dependencies are correctly
    installed, and the necessary database and file structures are in place.
"""
import customtkinter as ctk
from sidebar import SideBarFrame
from generator import Generator, EntryFrame
import pyperclip
import webbrowser
import constants as const
import logging
from database import DataBase
from encryption import EncryptionManager

logging.basicConfig(level=logging.DEBUG, filename=const.LOGGING_PATH,
                    format="%(asctime)s -  %(levelname)s - Module: %(module)s - %(message)s")
logger = logging.getLogger(__name__)


class Storage(ctk.CTkFrame):
    """
    Storage Class

    Represents a frame that serves as a component of a password storage and management system.
    This class includes features such as:
         creating, updating, and displaying user account details, a password generator.

    Attributes:
        - user_id (int): The unique identifier for the current user, retrieved from login auth.
        - new_item (ctk.CTkButton): Button for creating a new user account entry.
        - pw_generator (ctk.CTkButton): Button for launching the password generator.
        - log_out (ctk.CTkButton): Button for logging out of the application.
        - scrollable_frame (ctk.CTkScrollableFrame): Scrollable frame for displaying
          user account buttons.
        - details_frame (ctk.CTkFrame): Frame for displaying and editing account details.

    Methods:
        - open_toplevel(): Opens the password generator window.
        - open_entry_frame(): Opens the window for creating a new user account entry.
        - create_account_buttons(): Retrieves and displays user account buttons.
        - create_entry_widgets(account_name): Creates entry widgets based on account details.
        - destroy_entry_widgets(): Destroys entry widgets in the details frame.
        - destroy_account_buttons(): Destroys user account buttons in the scrollable frame.
        - show_details(account_index): Displays details for a selected user account.
        - create_entry_fields_and_buttons(): Creates entry fields and buttons for details.
        - fetch_and_display_details(account_index): Fetches and displays account details.
        - get_id_for_update(current_id): Retrieves the database ID for updating details.
        - update_details(): Updates user account details in the database.
        - copy_username(): Copies the username to the clipboard.
        - copy_password(): Copies the password to the clipboard.
        - open_website(): Opens the website associated with the selected account.
        - open_new_entry_frame(): Opens the window for creating a new user account entry.
        - set_user_id(user_id): Sets the user_id attribute.

    Usage:
        Instantiate this class within a customtkinter application to integrate a password
        storage and management system into the user interface.
    """
    def __init__(self, parent, controller, user_id):
        """
        Initializes the Storage instance.

        Parameters:
            - parent: The parent widget.
            - controller: The main frame switching controller.
            - user_id (int): The unique identifier for the current user.
        """
        ctk.CTkFrame.__init__(self, parent)

        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        sidebar.label("Storage Module")

        self.user_id = user_id
        self.db_path = const.DATABASE_PATH

        self.new_item = ctk.CTkButton(sidebar.frame, text="New Entry",
                                      command=self.open_entry_frame)
        self.new_item.grid(row=2, column=0, padx=20, pady=10)
        self.entry_window = None

        self.pw_generator = ctk.CTkButton(sidebar.frame, text="Pass Generator",
                                          command=self.open_toplevel)
        self.pw_generator.grid(row=3, column=0, padx=20, pady=10)
        self.toplevel_window = None

        self.log_out = ctk.CTkButton(sidebar.frame, text="Log Out",
                                     command=lambda: self.log_out_button_press(controller))
        self.log_out.grid(row=5, column=0, padx=20, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Accounts")
        self.scrollable_frame.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="ns")
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        self.details_frame = ctk.CTkFrame(self, width=400, height=500)
        self.details_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

    def log_out_button_press(self, controller):
        """
        Deletes all the buttons when the logout button is pressed
        """
        self.destroy_entry_widgets()
        controller.show_frame("Login")

    def open_toplevel(self):
        """
        Opens the window for password generator.
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Generator(self)
        else:
            self.toplevel_window.focus()

    def open_entry_frame(self):
        """
        Opens the window for creating a new user account entry.
        """
        if self.entry_window is None or not self.entry_window.winfo_exists():
            self.entry_window = EntryFrame(self, self.create_account_buttons, self.user_id)
        else:
            self.entry_window.focus()

    def create_account_buttons(self):
        """
        Retrieves data and creates account entry buttons.
        """

        logger.debug("The value inside Storage is: %s", self.user_id)

        with DataBase() as db:
            account_names = db.storage_create_account_buttons(self.user_id)

        self.destroy_account_buttons()

        for i, account_name in enumerate(account_names):
            button = ctk.CTkButton(master=self.scrollable_frame, text=account_name[0],
                                    command=lambda i=i: self.show_details(i))
            button.grid(row=i, column=0, padx=10, pady=(0, 20))

            # When the button is clicked, create entry widgets
            button.bind("<Button-1>", lambda event, account_name=account_name[0]:
                        self.create_entry_widgets(account_name))

    def create_entry_widgets(self, account_name):
        """
        Creates entry widgets based on account details.

        Parameters:
            - account_name: The name of the user account.
        """
        # Destroy previous widgets in the details frame
        self.destroy_entry_widgets()
        # Fetch account details based on the provided account_name
        with DataBase() as db:
            account_details = db.storage_fetch_user_data(account_name, self.user_id)
            encryption_key_tuple = db.storage_retrieve_encryption_key(self.user_id)

            encrypted_password = account_details[3]
            iv = account_details[5]
            encryption_key = encryption_key_tuple[0]
            encryption_manager = EncryptionManager(encryption_key)
            password = encryption_manager.decrypt(iv, encrypted_password)



        if account_details:
            self.current_id = account_details[0]

            self.name_entry = ctk.CTkEntry(self.details_frame)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
            self.name_entry.insert(0, account_details[1])

            self.username_entry = ctk.CTkEntry(self.details_frame)
            self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
            self.username_entry.insert(0, account_details[2])

            self.password_entry = ctk.CTkEntry(self.details_frame, show="*")
            self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")
            self.password_entry.insert(0, password)

            self.website_entry = ctk.CTkEntry(self.details_frame)
            self.website_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
            self.website_entry.insert(0, account_details[4])

            self.save_button = ctk.CTkButton(self.details_frame, text="Save",
                                             command=self.update_details)
            self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

            self.delete_button = ctk.CTkButton(self.details_frame, text="Delete",
                                               command=self.delete_details)
            self.delete_button.grid(row=6, column=0, columnspan=2, pady=10)

            self.copy_username_button = ctk.CTkButton(self.details_frame, text="Copy Username",
                                                      command=self.copy_username)
            self.copy_username_button.grid(row=1, column=2, padx=10, pady=10)

            self.copy_password_button = ctk.CTkButton(self.details_frame, text="Copy Password",
                                                      command=self.copy_password)
            self.copy_password_button.grid(row=2, column=2, padx=10, pady=10)

            self.open_website_button = ctk.CTkButton(self.details_frame, text="Open Website",
                                                     command=self.open_website)
            self.open_website_button.grid(row=3, column=2, padx=10, pady=10)

            self.details_frame.grid_propagate(False)

    def destroy_entry_widgets(self):
        """
        Destroys entry widgets in the details frame.
        """
        for widget in self.details_frame.winfo_children():
            widget.grid_remove()

    def destroy_account_buttons(self):
        """
        Destroys user account buttons in the scrollable frame.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_details(self, account_index):
        """
        Displays details for a selected user account.

        Parameters:
            - account_index: The index of the selected user entry.
        """
        self.create_entry_fields_and_buttons()
        self.fetch_and_display_details(account_index)

    def create_entry_fields_and_buttons(self):
        """
        Creates entry fields and buttons for details.
        """
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.entry_widgets = {}

        fields = ["name", "username", "password", "website"]
        for i, field in enumerate(fields):
            label = ctk.CTkLabel(self.details_frame, text=field.capitalize() + ":")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(self.details_frame)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="e")

            self.entry_widgets[field] = entry

        self.save_button = ctk.CTkButton(self.details_frame, text="Save",
                                        command=self.update_details)
        self.save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.details_frame.grid_propagate(False)

    def fetch_and_display_details(self, account_index=None):
        """
        Fetches and displays account details.

        Parameters:
            - account_index: The index of the selected user entry.
        """

        if account_index is not None:
            with DataBase() as db:
                account_details = db.storage_fetch_details(account_index)
                encryption_key_tuple = db.storage_retrieve_encryption_key(self.user_id)

            if account_details:
                self.create_entry_fields_and_buttons()

                name, username, encrypted_password, website, iv = account_details
                encryption_key = encryption_key_tuple[0]
                encryption_manager = EncryptionManager(encryption_key)
                password = encryption_manager.decrypt(iv, encrypted_password)

                # Update the entry widgets with fetched details
                self.entry_widgets["name"].delete(0, "end")
                self.entry_widgets["name"].insert(0, name)

                self.entry_widgets["username"].delete(0, "end")
                self.entry_widgets["username"].insert(0, username)

                self.entry_widgets["password"].delete(0, "end")
                self.entry_widgets["password"].insert(0, password)

                self.entry_widgets["website"].delete(0, "end")
                self.entry_widgets["website"].insert(0, website)
            else:
                logger.error("No account details found for the selected account index")

    def update_details(self):
        """
        Updates user account details in the database.
        """
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        website = self.website_entry.get()

        if self.current_id is not None:
            with DataBase() as db:
                encryption_key_tuple = db.storage_retrieve_encryption_key(self.user_id)
                encryption_key = encryption_key_tuple[0]
                encryption_manager = EncryptionManager(encryption_key)
                iv, encrypted_password = encryption_manager.encrypt(password)

                data = (name, username, encrypted_password, website, iv, self.current_id)
                db.storage_update_user_data(data)
                logger.info("Details updated successfully to the db.")

            self.create_account_buttons()

        else:
            logger.error("Record not found for the given ID.")

    def delete_details(self):

        if self.current_id is not None:
            with DataBase() as db:
                db.storage_delete_details(self.current_id)
            self.create_account_buttons()
            self.destroy_entry_widgets()

    def copy_username(self):
        """
        Copies the username to the clipboard.
        """
        username = self.username_entry.get()
        pyperclip.copy(username)

    def copy_password(self):
        """
        Copies the password to the clipboard.
        """
        password = self.password_entry.get()
        pyperclip.copy(password)

    def open_website(self):
        """
        Opens the website associated with the selected account.
        """
        website = self.website_entry.get()
        webbrowser.open(website)

    def open_new_entry_frame(self):
        """
        Opens the window for creating a new user account entry.
        It uses EntryFrame Class from the generator module
        """
        EntryFrame(self, self.create_account_buttons, self.user_id)

    def set_user_id(self, user_id):
        """
        Used inside the main module to set the user ID from the login authentication.

        Parameters:
            - user_id: The new user ID to set.
        """
        self.user_id = user_id

