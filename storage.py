import customtkinter as ctk
import os
from sidebar import SideBarFrame
from generator import Generator, EntryFrame
import sqlite3
import pyperclip
import webbrowser

class Storage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)


        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        sidebar.label("Storage Module")

        self.user_id = 2

        self.new_item = ctk.CTkButton(sidebar.frame, text="New Entry", command=self.open_entry_frame)
        self.new_item.grid(row=2, column=0, padx=20, pady=10)
        self.entry_window = None

        self.pw_generator = ctk.CTkButton(sidebar.frame, text="Pass Generator", command=self.open_toplevel)
        self.pw_generator.grid(row=3, column=0, padx=20, pady=10)
        self.toplevel_window = None

        self.log_out = ctk.CTkButton(sidebar.frame, text="Log Out", command=lambda: controller.show_frame("Login"))
        self.log_out.grid(row=5, column=0, padx=20, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Accounts")
        self.scrollable_frame.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="ns")
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        self.details_frame = ctk.CTkFrame(self, width=400, height=500)
        self.details_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self.create_account_buttons()

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Generator(self)
        else:
            self.toplevel_window.focus()

    def open_entry_frame(self):
        if self.entry_window is None or not self.entry_window.winfo_exists():
            self.entry_window = EntryFrame(self, self.create_account_buttons)
        else:
            self.entry_window.focus()

    def create_account_buttons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        with sqlite3.connect(self.db_path) as connection:
            connect = sqlite3.connect(self.db_path)
            cursor = connect.cursor()


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

        cursor.execute("SELECT entry_name FROM UserData WHERE User_id=?", [self.user_id])
        account_names = cursor.fetchall()

        connection.close()

        self.destroy_account_buttons()

        for i, account_name in enumerate(account_names):
            button = ctk.CTkButton(master=self.scrollable_frame, text=account_name[0], command=lambda i=i: self.show_details(i))
            button.grid(row=i, column=0, padx=10, pady=(0, 20))

            # When the button is clicked, create entry widgets with the expected structure
            button.bind("<Button-1>", lambda event, account_name=account_name[0]: self.create_entry_widgets(account_name))

    def create_entry_widgets(self, account_name):
        # Destroy previous widgets in the details frame
        self.destroy_entry_widgets()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")


        # Fetch account details based on the provided account_name
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT entry_id, entry_name, entry_username, entry_password, entry_website FROM UserData WHERE entry_name=? AND User_id=?", (account_name, self.user_id))
        account_details = cursor.fetchone()
        conn.close()

        if account_details:
            self.current_id = account_details[0]
            print(self.current_id)
            # Create entry widgets with the fetched details
            self.name_entry = ctk.CTkEntry(self.details_frame)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
            self.name_entry.insert(0, account_details[1])

            self.username_entry = ctk.CTkEntry(self.details_frame)
            self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
            self.username_entry.insert(0, account_details[2])

            self.password_entry = ctk.CTkEntry(self.details_frame, show="*")
            self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")
            self.password_entry.insert(0, account_details[3])

            self.website_entry = ctk.CTkEntry(self.details_frame)
            self.website_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
            self.website_entry.insert(0, account_details[4])

            self.save_button = ctk.CTkButton(self.details_frame, text="Save", command=self.update_details)
            self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

            self.copy_username_button = ctk.CTkButton(self.details_frame, text="Copy Username", command=self.copy_username)
            self.copy_username_button.grid(row=1, column=2, padx=10, pady=10)

            self.copy_password_button = ctk.CTkButton(self.details_frame, text="Copy Password", command=self.copy_password)
            self.copy_password_button.grid(row=2, column=2, padx=10, pady=10)

            self.open_website_button = ctk.CTkButton(self.details_frame, text="Open Website", command=self.open_website)
            self.open_website_button.grid(row=3, column=2, padx=10, pady=10)

            self.details_frame.grid_propagate(False)

    def destroy_entry_widgets(self):
        for widget in self.details_frame.winfo_children():
            widget.grid_remove()

    def destroy_account_buttons(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_details(self, account_index):
        print("Show details called")
        self.create_entry_fields_and_buttons()
        self.fetch_and_display_details(account_index)

    def create_entry_fields_and_buttons(self):
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

        self.save_button = ctk.CTkButton(self.details_frame, text="Save", command=self.update_details)
        self.save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.details_frame.grid_propagate(False)


    #! This will not work
    def fetch_and_display_details(self, account_index=None):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if account_index is not None:
            cursor.execute("SELECT entry_name, entry_username, entry_password, entry_website FROM UserData LIMIT 1 OFFSET ?", (account_index,))
            account_details = cursor.fetchone()

            print(f"Fetched details from database - {account_details}")

            if account_details:
                # Ensure entry widgets are created
                self.create_entry_fields_and_buttons()

                name, username, password, website = account_details

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
                print("No account details found for the selected account index.")

        conn.close()

    def get_id_for_update(self, current_id):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Fetch the id based on the current_id
        cursor.execute("SELECT entry_id FROM UserData WHERE entry_id=?", (current_id,))
        result = cursor.fetchone()

        # Print statements for debugging
        print(f"Current ID: {current_id}")
        print(f"SQL Query result: {result}")

        # Close the database connection
        conn.close()

        if result:
            return result[0]  # Return the id
        else:
            # Handle the case where the current_id is not found
            return None

    def update_details(self):
        # Get values from entry widgets
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        website = self.website_entry.get()

        # Get the id for the update
        current_id = self.get_id_for_update(self.current_id)  # Use self.current_id here

        if current_id is not None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            database_folder = os.path.join(script_dir, "database")
            os.makedirs(database_folder, exist_ok=True)
            self.db_path = os.path.join(database_folder, "AccessControlDB.db")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Update the database with the new values using the current_id
            cursor.execute("UPDATE UserData SET entry_name=?, entry_username=?, entry_password=?, entry_website=? WHERE entry_id=?", (name, username, password, website, current_id))

            # Commit the changes to the database
            conn.commit()

            # Close the database connection
            conn.close()

            print("Details updated successfully.")

            self.create_account_buttons()

        else:
            print("Record not found for the given ID.")

    def copy_username(self):
        username = self.username_entry.get()
        print(f"{username}")
        pyperclip.copy(username)

    def copy_password(self):
        password = self.password_entry.get()
        pyperclip.copy(password)

    def open_website(self):
        website = self.entry_widgets["website"].get()
        webbrowser.open(website)

    def open_new_entry_frame(self):
        print(f'{self.user_id}')
        EntryFrame(self, self.create_account_buttons)
