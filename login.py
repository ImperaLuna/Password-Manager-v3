import customtkinter as ctk
from sidebar import SideBarFrame
import sqlite3
import bcrypt
import os



class Login(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        from register import Register
        from storage import Storage

        # Create an instance of SideBarFrame
        sidebar = SideBarFrame(self, controller)
        sidebar.grid(row=0, column=0, rowspan=4, sticky='ns')
        sidebar.label('Login')





        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, 'user_credentials.db')

        self.login_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.login_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky='nsw')
        self.login_frame.grid_columnconfigure(0, weight=0)
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        self.username = ctk.CTkEntry(master=self.login_frame, placeholder_text="Username")
        self.username.grid(row=0, column=0, pady=12, padx=10, sticky='ew')  # Use grid for username

        self.password = ctk.CTkEntry(master=self.login_frame, placeholder_text="Password", show="*")
        self.password.grid(row=1, column=0, pady=12, padx=10, sticky='ew')  # Use grid for password

        checkbox = ctk.CTkCheckBox(master=self.login_frame, text="Remember Me")
        checkbox.grid(row=2, column=0, pady=6, padx=50, sticky='ew')

        button = ctk.CTkButton(master=self.login_frame, text="Login", command=self.login)
        button.grid(row=3, column=0, pady=6, padx=50, sticky='ew')

        register = ctk.CTkButton(master=self.login_frame, text='Register',  
                                 command=lambda: controller.show_frame(Register))
        register.grid(row=5, column=0, pady=6, padx=50, sticky='ew')

        self.error_label = ctk.CTkLabel(self.login_frame, text='', fg_color='transparent')  # Fix variable scope
        self.error_label.grid(row=6, column=0, padx=12, sticky='ew')

        #! skip login button
        button_skip = ctk.CTkButton(master=self.login_frame, text='Skip Login',
                                    command=lambda: controller.show_frame(Storage))
        button_skip.grid(row=7, column=0, padx=12, sticky='ew')

    # Login Logic
    def login(self):
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()

        username_input = self.username.get()
        password_input = self.password.get()

        try:
            if not username_input or not password_input:
                self.error_label.configure(text='Please enter username and password', fg_color='red')
                return
            
            cursor.execute('SELECT Password FROM credentials where Username=?', [username_input,])  # Fix the missing comma
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password_input.encode('utf-8'), result[0]):
                    print('login correct')
                    self.master.switch_to_generator_window()
                else:
                    print('login failed')
            else:
                print('invalid username')
        except Exception as e:
            print(f"Error: {e}")


