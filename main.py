import customtkinter as ctk
from login import Login
from register import Register
from storage import Storage


ctk.set_appearance_mode('system')
ctk.set_default_color_theme('orange')



class MainApp(ctk.CTk):
    def __init__(self): 
        ctk.CTk.__init__(self)



        self.title('Password Manager')
        self.geometry('960x540')
        self.resizable(False, False)

        container = ctk.CTkFrame(self) 
        container.grid()



        self.frames = {} 
        for WINDOW in (Login, Register, Storage):

            frame = WINDOW(container, self)
            self.frames[WINDOW] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
