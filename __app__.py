import customtkinter
from customtkinter import *

import constants
from components.frames import HomeFrame

customtkinter.set_appearance_mode(constants.APPEARANCE_MODE)
customtkinter.set_default_color_theme(constants.COLOR_THEME)


class App(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title(constants.TITLE)
        self.geometry(f'{constants.WIDTH}x{constants.HEIGHT}')

        self.homeFrame = HomeFrame(master=self)
        self.homeFrame.pack(anchor=CENTER, expand=True, fill=BOTH, pady=50, padx=50)
        self.mainloop()
