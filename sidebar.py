import customtkinter as ctk


#todo make method to add upper/lower buttons
class SideBarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        grey = '#212121'

        #! Bug : Next 3 lines are required in order for the sideframe to be displayed properly...
        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0 )
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.frame.grid_rowconfigure(4, weight=1)

        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0, fg_color=grey)
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = ctk.CTkLabel(self.frame, text='Appearance Mode:', anchor='sw')
        self.appearance_mode_label.grid(row=6, column=0, padx=40, pady=(0, 10), sticky='sw')

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.frame, values=['System', 'Light', 'Dark'],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=40, pady=(0, 40), sticky='sw')


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)



    def label(self, text):
        self.logo_label = ctk.CTkLabel(self.frame, text=f'{text}', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))
