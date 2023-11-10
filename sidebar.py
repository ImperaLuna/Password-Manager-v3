import customtkinter as ctk

grey = '#212121'

class SideBarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        
        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0 )
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')  
        self.frame.grid_rowconfigure(4, weight=1)

        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0, fg_color=grey)
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')  
        self.frame.grid_rowconfigure(4, weight=1)