import sqlite3
import bcrypt
import os
import customtkinter as ctk
from sidebar import SideBarFrame
import json
from cryptography.fernet import Fernet

class Login(ctk.CTkFrame):
    def __init__(self, parent, controller, user_id):
        ctk.CTkFrame.__init__(self, parent)

       # Create an instance of SideBarFrame
        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        sidebar.label("Login")

        self.user_id = None

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")

        self.login_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.login_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsw")
        self.login_frame.grid_columnconfigure(0, weight=0)
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        self.username = ctk.CTkEntry(master=self.login_frame, placeholder_text="Username")
        self.username.grid(row=0, column=0, pady=12, padx=10, sticky="ew")

        self.password = ctk.CTkEntry(master=self.login_frame, placeholder_text="Password", show="*")
        self.password.grid(row=1, column=0, pady=12, padx=10, sticky="ew")

        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(master=self.login_frame, text="Remember Me", variable=self.checkbox_var)
        self.checkbox.grid(row=2, column=0, pady=6, padx=50, sticky="ew")
        self.check_credentials_file()

        button = ctk.CTkButton(master=self.login_frame, text="Login",
                                command=lambda: self.login(controller, "Storage"))

        button.grid(row=3, column=0, pady=6, padx=50, sticky="ew")

        register = ctk.CTkButton(master=self.login_frame, text="Register",
                                command=lambda: controller.show_frame("Register"))
        register.grid(row=5, column=0, pady=6, padx=50, sticky="ew")

        self.error_label = ctk.CTkLabel(self.login_frame, text="",
                                         fg_color="transparent")  # Fix variable scope
        self.error_label.grid(row=6, column=0, padx=12, sticky="ew")

        #! skip login button
        button_skip = ctk.CTkButton(master=self.login_frame, text="Skip Login",
                                    command=lambda: controller.show_frame("Storage"))
        button_skip.grid(row=7, column=0, padx=12, sticky="ew")

    def login(self, controller, storage_class):
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()

        checkbox_execute = self.checkbox_var.get()
        username_input = self.username.get()
        password_input = self.password.get()

        try:
            if not username_input or not password_input:
                self.error_label.configure(text="Please enter username and password", fg_color="red")
                return

            cursor.execute("SELECT ID, Password FROM Users WHERE Username=?", [username_input,])
            result = cursor.fetchone()

            if result:
                user_id, hashed_password = result
                if bcrypt.checkpw(password_input.encode("utf-8"), hashed_password):
                    self.save_user_id(user_id)
                    controller.show_frame(storage_class)



                    # Save credentials if the "Remember Me" checkbox is checked
                    if checkbox_execute:
                        self.save_credentials(username_input, password_input)
                    else:
                        self.delete_credentials()
                        self.clear_login()

                else:
                    self.error_label.configure(text="Invalid password", fg_color="red")
            else:
                self.error_label.configure(text="Invalid username", fg_color="red")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connect.close()

    def save_credentials(self, username, password):
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()


        cursor.execute("SELECT encryption_key FROM Users WHERE Username=?", [username])
        db_encryption_key = cursor.fetchone()
        encryption_key = db_encryption_key[0]

        if not encryption_key:
            encryption_key = Fernet.generate_key()
            cursor.execute("UPDATE Users SET Encryption_key=? WHERE Username=?", [encryption_key, username])
            connect.commit()


        # Encrypt the password using the key
        fernet = Fernet(encryption_key)
        encrypted_password = fernet.encrypt(password.encode("utf-8")).decode("utf-8")


        credentials = {"username": username, "password": encrypted_password}
        db_folder = os.path.dirname(self.db_path)
        credentials_path = os.path.join(db_folder, "credentials.json")
        with open(credentials_path, "w") as f:
            json.dump(credentials, f)

    def check_credentials_file(self):
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()

        try:
            db_folder = os.path.dirname(self.db_path)
            credentials_path = os.path.join(db_folder, "credentials.json")
            with open(credentials_path, "r") as f:
                credentials = json.load(f)
                username, encrypted_password = credentials.get("username", ""), credentials.get("password", "")

                cursor.execute("SELECT encryption_key FROM Users WHERE Username=?", [username])
                db_encryption_key = cursor.fetchone()
                encryption_key = db_encryption_key[0]

                fernet = Fernet(encryption_key)
                password = fernet.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")

                self.username.insert(ctk.END, username)
                self.password.insert(ctk.END, password)

                self.checkbox_var.set(True)

        except FileNotFoundError:
            self.checkbox_var.set(False)

    def delete_credentials(self):
        db_folder = os.path.dirname(self.db_path)
        db_credentials_path = os.path.join(db_folder, "credentials.json")
        try:
            os.remove(db_credentials_path)
        except FileNotFoundError:
            pass

    def clear_login(self):
        checkbox_execute = self.checkbox_var.get()

        if not checkbox_execute:
            self.username.delete(0, ctk.END)
            self.password.delete(0, ctk.END)

    def save_user_id(self, user_id):
        self.user_id = user_id
        print(f'user id is:{user_id}')

    def get_user_id(self):
        return self.user_id

