import customtkinter as ctk
from login import Login
import os
import sqlite3
import bcrypt

class Register(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
		
        self.sidebar_frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky='ns')  
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky='ns')  
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        


        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Register Form', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.back_to_login = ctk.CTkButton(self.sidebar_frame,text='Back To Login', 
                                           command = lambda : controller.show_frame(Login))
        self.back_to_login.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text='Appearance Mode:', anchor='sw')
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(20, 10), sticky='sw')  

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['System','Light', 'Dark'], 
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(0, 40), sticky='sw')  
                
        # create register form
        self.register_form_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.register_form_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky='nsw')
        self.register_form_frame.grid_columnconfigure(0, weight=0)
        self.register_form_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        self.username = ctk.CTkEntry(master=self.register_form_frame, placeholder_text='Username')
        self.username.grid(row=0, column=0, pady=12, padx=80, sticky='ew')

        self.password = ctk.CTkEntry(master=self.register_form_frame, placeholder_text='Password', show='*')
        self.password.grid(row=1, column=0, pady=12, padx=80, sticky='ew')

        self.repeat_password = ctk.CTkEntry(master=self.register_form_frame, placeholder_text='Repeat Password', show='*')
        self.repeat_password.grid(row=2, column=0, pady=12, padx=80, sticky='ew')

        self.checkbox_var = ctk.StringVar(value='off')  # Initialize checkbox value as 'off'
        self.checkbox = ctk.CTkCheckBox(master=self.register_form_frame, text='Show Password',
                                         command=self.reveal_password, variable= self.checkbox_var,
                                         onvalue='on', offvalue='off')
        self.checkbox.grid(row=3, column=0, pady=0, padx=80, sticky='ew')  

        self.button_register = ctk.CTkButton(master=self.register_form_frame, text='Register', 
                                             command=self.button_register_event)
        self.button_register.grid(row=4, column=0, pady=6, padx=120, sticky='ew')

        self.error_label = ctk.CTkLabel(self.register_form_frame, text='', fg_color='transparent')
        self.error_label.grid(row=5, column=0, padx=80, sticky='ew')  


        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, 'user_credentials.db')
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (Username TEXT NOT NULL, Password TEXT NOT NULL) ''')

    def button_register_event(self):
        username = self.username.get()
        password = self.password.get()
        repeat_password = self.repeat_password.get()

        #User input handling
        try:
            if not username or not password or not repeat_password:
                self.error_label.configure(text='Please fill in all fields', fg_color='red')
                return

            if password != repeat_password:
                self.error_label.configure(text="Passwords do not match", fg_color='red')
                return
            
            # Register User
            self.cursor.execute('SELECT username FROM credentials WHERE username=?', [username])
            if self.cursor.fetchone() is not None:
                self.error_label.configure(text="Username already exists", fg_color='red')
                return
            
            else:
                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                self.cursor.execute('INSERT INTO credentials VALUES(?, ?)', [username, hashed_password])

                self.connect.commit()
                self.error_label.configure(text='Account has been created', fg_color='green')

        except Exception as e:
             print(f"Error: {e}")
             self.error_label.configure(text="An error occurred during registration.", fg_color='red')

    def reveal_password(self):
        
        show_text = self.checkbox_var.get() == 'on'
        if show_text:
            self.password.configure(show='')
            self.repeat_password.configure(show='')
        else:
            self.password.configure(show='*')
            self.repeat_password.configure(show='*')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

