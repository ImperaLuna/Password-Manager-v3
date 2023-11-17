"""
This module defines the SideBarFrame class, which is a customtkinter frame for creating a sidebar.
The sidebar includes options for appearance mode and additional labels.

Classes:
- SideBarFrame: A custom Tkinter frame for creating a sidebar in a GUI.

Usage:
1. Create an instance of SideBarFrame in your GUI application.
2. Customize the appearance mode options and labels as needed.
"""
import customtkinter as ctk


#todo make method to add upper/lower buttons
class SideBarFrame(ctk.CTkFrame):
    """
    SideBarFrame - A customtkinter frame for creating a sidebar in a graphical user interface (GUI).

    Attributes:
    - parent: The parent widget for this frame.
    - appearance_mode_label: Label displaying the "Appearance Mode" text in the sidebar.
    - appearance_mode_optionemenu: OptionMenu widget for selecting appearance modes.
    - logo_label: Label for displaying labeled sections in the sidebar.

    Methods:
    - change_appearance_mode_event: Change the appearance mode of the GUI.
    - label(self, text): Add a labeled section to the sidebar.

    Usage:
    1. Create an instance of SideBarFrame in your GUI application.
    2. Customize the appearance mode options and labels as needed.
    """
    def __init__(self, parent): # do i need to add controller?
        ctk.CTkFrame.__init__(self, parent)
        grey = '#212121'

        #! Bug : Next 3 lines are required in order for the side frame to be displayed properly...
        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0 )
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.frame.grid_rowconfigure(4, weight=1)

        self.frame = ctk.CTkFrame(self, width=140, height=560, corner_radius=0, fg_color=grey)
        self.frame.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = ctk.CTkLabel(self.frame, text='Appearance Mode:', anchor='sw')
        self.appearance_mode_label.grid(row=6, column=0, padx=40, pady=(0, 10), sticky='sw')

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.frame,
                                                            values=['System', 'Light', 'Dark'],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=40, pady=(0, 40), sticky='sw')


    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Method used to change the appearance_mode to system/dark/light mode
        """
        ctk.set_appearance_mode(new_appearance_mode)



    def label(self, text):
        """
        Method used to set the text label for the sidebar
        """
        self.logo_label = ctk.CTkLabel(self.frame, text=f'{text}',
                                    font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))
