import customtkinter as ctk
import random
import string

class Generator(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

# create textbox
        self.textbox = ctk.CTkTextbox(self, width=100)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # text for Pasword
        title = "Generated Password:"
        self.textbox.insert("1.0", title + "\n")
        self.textbox.insert("2.0", "")

        # create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        checkbox_label = ctk.CTkLabel(master=self.checkbox_slider_frame, text="Password Strength")
        checkbox_label.pack()

        # create variables to store checkbox states
        self.checkbox_1_var = ctk.BooleanVar()
        self.checkbox_2_var = ctk.BooleanVar()
        self.checkbox_3_var = ctk.BooleanVar()
        self.checkbox_4_var = ctk.BooleanVar()

        self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Lowercase letters", variable=self.checkbox_1_var)
        self.checkbox_1.pack(anchor="w", padx=20, pady=(20, 0))
        self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Uppercase letters", variable=self.checkbox_2_var)
        self.checkbox_2.pack(anchor="w", padx=20, pady=(20, 0))
        self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Numbers", variable=self.checkbox_3_var)
        self.checkbox_3.pack(anchor="w", padx=20, pady=(20, 0))
        self.checkbox_4 = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text="Symbols", variable=self.checkbox_4_var)
        self.checkbox_4.pack(anchor="w", padx=20, pady=(20, 0))

        self.checkbox_1_var.set(True)
        
        # create generate button
        self.generate_button = ctk.CTkButton(master=self.checkbox_slider_frame, text="Generate", command=self.generate_new_password)
        self.generate_button.pack(anchor="w", padx=20, pady=(20, 0))

    def generate_password(self, length=8, use_lowercase=True, use_uppercase=True, use_numbers=True, use_symbols=True):
        characters = ""

        if use_lowercase:
            characters += string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation.replace('"', '').replace("'", "")

        password = "".join(random.choice(characters) for _ in range(length)) 
        return password

    def generate_new_password(self):
        if not any([self.checkbox_1_var.get(), self.checkbox_2_var.get(), self.checkbox_3_var.get(), self.checkbox_4_var.get()]):
            self.textbox.delete("2.0", "end-1c")
            self.textbox.insert("2.0", "Please select at least one option.")

        use_lowercase = self.checkbox_1_var.get()
        use_uppercase = self.checkbox_2_var.get()
        use_numbers = self.checkbox_3_var.get()
        use_symbols = self.checkbox_4_var.get()

        generated_password = self.generate_password(
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols)
        self.textbox.delete("2.0", "end-1c")  # Clear the existing generated password
        self.textbox.insert("2.0", generated_password)