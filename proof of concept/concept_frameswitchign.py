import customtkinter as ctk

LARGEFONT = ("Verdana", 35)

class tkinterApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        button1 = ctk.CTkButton(self, text="Page 1", command=lambda: controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = ctk.CTkButton(self, text="Page 2", command=lambda: controller.show_frame(Page2))
        button2.grid(row=2, column=1, padx=10, pady=10)

class Page1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        button1 = ctk.CTkButton(self, text="StartPage", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = ctk.CTkButton(self, text="Page 2", command=lambda: controller.show_frame(Page2))
        button2.grid(row=2, column=1, padx=10, pady=10)

class Page2(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        button1 = ctk.CTkButton(self, text="Page 1", command=lambda: controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = ctk.CTkButton(self, text="Startpage", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=2, column=1, padx=10, pady=10)

app = tkinterApp()
app.mainloop()
