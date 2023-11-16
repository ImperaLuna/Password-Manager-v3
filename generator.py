import customtkinter as ctk
import os
import random
import string
import sqlite3
import pyperclip

class Generator(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("490x430")
        self.resizable(False, False)


        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=50, height=10)
        self.textbox.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # text for Password
        title = "Generated Password:"
        self.textbox.insert("1.0", title + "\n")
        self.textbox.insert("2.0", "")
        # create copy button
        self.copy_button = ctk.CTkButton(master=self.textbox, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="w")

        # create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        checkbox_label = ctk.CTkLabel(master=self.checkbox_slider_frame, text="Password Strength")
        checkbox_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), columnspan=2)

        # create slider for password length
        self.length_slider_label = ctk.CTkLabel(master=self.checkbox_slider_frame, text="Password Length:")
        self.length_slider_label.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")

        self.length_var = ctk.IntVar()
        self.length_slider = ctk.CTkSlider(master=self.checkbox_slider_frame, from_=8, to=48, variable=self.length_var, width=200)
        self.length_slider.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")
        self.length_var.set(8)  # Set default value

        # display the selected length
        self.length_display_label = ctk.CTkLabel(master=self.checkbox_slider_frame, text="Selected Length: 8")
        self.length_display_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        # update the label when the slider value changes
        self.length_slider.bind("<B1-Motion>", lambda event: self.update_length_display())
        self.length_slider.bind("<ButtonRelease-1>", lambda event: self.update_length_display())

        # create generate button
        self.generate_button = ctk.CTkButton(master=self.checkbox_slider_frame, text="Generate", command=self.generate_new_password)
        self.generate_button.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="w")

        # create variables to store checkbox states
        self.checkbox_1_var = ctk.BooleanVar()
        self.checkbox_2_var = ctk.BooleanVar()
        self.checkbox_3_var = ctk.BooleanVar()
        self.checkbox_4_var = ctk.BooleanVar()

        self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Lowercase letters", variable=self.checkbox_1_var)
        self.checkbox_1.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="w")
        self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Uppercase letters", variable=self.checkbox_2_var)
        self.checkbox_2.grid(row=6, column=0, padx=20, pady=(20, 0), sticky="w")
        self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Numbers", variable=self.checkbox_3_var)
        self.checkbox_3.grid(row=7, column=0, padx=20, pady=(20, 0), sticky="w")
        self.checkbox_4 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Symbols", variable=self.checkbox_4_var)
        self.checkbox_4.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="w")

        self.checkbox_1_var.set(True)

    def generate_password(self, length=8, use_lowercase=True, use_uppercase=True, use_numbers=True, use_symbols=True):
        characters = ""
        password = ""

        if use_lowercase:
            characters += string.ascii_lowercase
            password += random.choice(string.ascii_lowercase)
        if use_uppercase:
            characters += string.ascii_uppercase
            password += random.choice(string.ascii_uppercase)
        if use_numbers:
            characters += string.digits
            password += random.choice(string.digits)
        if use_symbols:
            characters += string.punctuation
            password += random.choice(string.punctuation)

        remaining_length = length - len(password)
        password += "".join(random.choice(characters) for _ in range(remaining_length))
        password_list = list(password)
        random.shuffle(password_list)
        password = "".join(password_list)

        return password


    def generate_new_password(self):
        if not any([self.checkbox_1_var.get(), self.checkbox_2_var.get(), self.checkbox_3_var.get(), self.checkbox_4_var.get()]):
            self.textbox.delete("2.0", "end-1c")
            self.textbox.insert("2.0", "Please select at least one option.")
        else:
            try:
                use_lowercase = self.checkbox_1_var.get()
                use_uppercase = self.checkbox_2_var.get()
                use_numbers = self.checkbox_3_var.get()
                use_symbols = self.checkbox_4_var.get()

                generated_password = self.generate_password(
                    length=self.length_var.get(),
                    use_lowercase=use_lowercase,
                    use_uppercase=use_uppercase,
                    use_numbers=use_numbers,
                    use_symbols=use_symbols)

                # Insert an empty line before the generated password
                self.textbox.delete("2.0", "end-1c")  # Clear the existing generated password
                self.textbox.insert("2.0", generated_password)
            except IndexError:
                # Handle the error gracefully (optional: you can print a message or leave it blank)
                pass


    def copy_to_clipboard(self):
        password = self.textbox.get("2.0", "end-1c")
        pyperclip.copy(password)

    def update_length_display(self):
        selected_length = self.length_var.get()
        self.length_display_label.configure(text=f"Selected Length: {selected_length}")

class EntryFrame(ctk.CTkToplevel):
    def __init__(self, master, refresh_callback):
        super().__init__(master)
        self.title("New Entry")
        self.resizable(False, False)
        self.user_id = 3

        self.name_label = ctk.CTkLabel(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.website_label = ctk.CTkLabel(self, text="Website:")
        self.website_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.website_entry = ctk.CTkEntry(self)
        self.website_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.save_button = ctk.CTkButton(self, text="Save", command=lambda: self.save_entry(refresh_callback))
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_entry(self, refresh_callback):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_folder = os.path.join(script_dir, "database")
        os.makedirs(database_folder, exist_ok=True)
        self.db_path = os.path.join(database_folder, "AccessControlDB.db")


        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO UserData (entry_name, entry_username, entry_password, entry_website, User_id) VALUES (?, ?, ?, ?, ?)',
                    (self.name_entry.get(), self.username_entry.get(), self.password_entry.get(), self.website_entry.get(), self.user_id))




        conn.commit()
        conn.close()

        self.destroy()
        refresh_callback()