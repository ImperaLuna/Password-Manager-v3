import customtkinter as ctk
import sqlite3
import pyperclip  
import webbrowser  

class Storage(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        
        from login import Login

        self.sidebar_frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky='ns')  
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky='ns')  
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Storage Module', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.new_item = ctk.CTkButton(self.sidebar_frame, text='New Entry')
        self.new_item.grid(row=1, column=0, padx=20, pady=10)

        self.log_out = ctk.CTkButton(self.sidebar_frame, text='Log Out', command=lambda: controller.show_frame(Login))
        self.log_out.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text='Appearance Mode:', anchor='sw')
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(20, 10), sticky='sw')

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['System', 'Light', 'Dark'],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=40, pady=(0, 20), sticky='sw')

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Accounts")
        self.scrollable_frame.grid(row=0, column=1, padx=(40, 0), pady=(20, 0), sticky="ns")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.details_frame = ctk.CTkFrame(self, width=400, height=500)  # Frame for displaying specific content
        self.details_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        # Prevent the details_frame from resizing
        self.details_frame.pack_propagate(False)

        # Create buttons for accounts
        self.create_account_buttons()

    def create_account_buttons(self):
        # Connect to the database
        conn = sqlite3.connect('db_test.db')
        cursor = conn.cursor()

        # Fetch account names from the database
        cursor.execute('SELECT name FROM accounts')
        account_names = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Create buttons for each account
        for i, account_name in enumerate(account_names):
            button = ctk.CTkButton(master=self.scrollable_frame, text=account_name[0], command=lambda i=i: self.show_details(i))
            button.grid(row=i, column=0, padx=10, pady=(0, 20))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def show_details(self, account_index):
        # Create entry fields and buttons dynamically
        self.create_entry_fields_and_buttons()

        # Fetch and display account details from the database based on the selected account
        self.fetch_and_display_details(account_index)


    def create_entry_fields_and_buttons(self):
        # Clear existing widgets in the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Create entries for name, username, password, and website
        self.name_entry = ctk.CTkEntry(self.details_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Continue with other entry fields and buttons
        self.username_label = ctk.CTkLabel(self.details_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.username_entry = ctk.CTkEntry(self.details_frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.password_label = ctk.CTkLabel(self.details_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = ctk.CTkEntry(self.details_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.website_label = ctk.CTkLabel(self.details_frame, text="Website:")
        self.website_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.website_entry = ctk.CTkEntry(self.details_frame)
        self.website_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.save_button = ctk.CTkButton(self.details_frame, text="Save", command=self.save_details)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.copy_username_button = ctk.CTkButton(self.details_frame, text="Copy Username", command=self.copy_username)
        self.copy_username_button.grid(row=1, column=2, padx=10, pady=10)

        self.copy_password_button = ctk.CTkButton(self.details_frame, text="Copy Password", command=self.copy_password)
        self.copy_password_button.grid(row=2, column=2, padx=10, pady=10)

        self.open_website_button = ctk.CTkButton(self.details_frame, text="Open Website", command=self.open_website)
        self.open_website_button.grid(row=3, column=2, padx=10, pady=10)

    def fetch_and_display_details(self, account_index=None):
        # Connect to the database
        conn = sqlite3.connect('db_test.db')
        cursor = conn.cursor()

        if account_index is not None:
            # Fetch account details from the database based on the selected account
            cursor.execute('SELECT name, username, password, website FROM accounts LIMIT 1 OFFSET ?', (account_index,))
            account_details = cursor.fetchone()

            if account_details:
                name, username, password, website = account_details

                # Display account details
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, name)

                self.username_entry.delete(0, 'end')
                self.username_entry.insert(0, username)

                self.password_entry.delete(0, 'end')
                self.password_entry.insert(0, password)

                self.website_entry.delete(0, 'end')
                self.website_entry.insert(0, website)

        # Close the database connection
        conn.close()

    def save_details(self):
        # Connect to the database
        conn = sqlite3.connect('db_test.db')
        cursor = conn.cursor()

        account_name = self.name_entry.get()

        cursor.execute('UPDATE accounts SET username=?, password=?, website=? WHERE name=?',
                        (self.username_entry.get(), self.password_entry.get(), self.website_entry.get(), account_name))

        conn.commit()
        conn.close()

    def copy_username(self):
        username = self.username_entry.get()
        pyperclip.copy(username)

    def copy_password(self):
        password = self.password_entry.get()
        pyperclip.copy(password)

    def open_website(self):
        website = self.website_entry.get()
        webbrowser.open(website)