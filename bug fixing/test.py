import customtkinter as ctk
import sqlite3

class MainApp(ctk.CTk):
    def __init__(self): 
        ctk.CTk.__init__(self)                                                                                      
        container = ctk.CTkFrame(self) 
        container.grid()
        self.geometry("200x200")

        self.entry = ctk.CTkEntry(container)  # Use container as the parent
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.save_button = ctk.CTkButton(container, text="Save", command=self.update_details)
        self.save_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_button = ctk.CTkButton(container, text="Update DB", command=self.save_to_database)
        self.update_button.grid(row=2, column=0, columnspan=2, pady=10)

    def update_details(self):
        # Connect to the database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Retrieve the record from the database
        cursor.execute("SELECT * FROM data")
        result = cursor.fetchone()
        if result:
            name_from_db, value_from_db = result
        else:
            name_from_db, value_from_db = "No Name", "No Value"

        # Close the database connection
        conn.close()

        # Update the entry widget with the retrieved value after a short delay
        self.after(100, lambda: self.update_entry(value_from_db))

        # Print the retrieved values
        print(f"Updating details with name: {name_from_db}, value: {value_from_db}")

    def update_entry(self, value):
        # Update the entry widget with the retrieved value
        self.entry.delete(0, 'end')  # Clear existing text
        self.entry.insert(0, value)

    def save_to_database(self):
        # Connect to the database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Get the value from the entry widget
        new_value = self.entry.get()

        # Update the database with the new value
        cursor.execute("UPDATE data SET value=? WHERE name=?", (new_value, "TestName"))
        conn.commit()

        # Close the database connection
        conn.close()

        print(f"Value updated in the database: {new_value}")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
