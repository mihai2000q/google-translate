import customtkinter
from customtkinter import *

from app.utilities import constants
from app.frames.home_frame import HomeFrame

TOP_LEVEL_ICON = 'google_translate_logo.ico'

customtkinter.set_appearance_mode(constants.APPEARANCE_MODE)
customtkinter.set_default_color_theme(constants.COLOR_THEME)


class App(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title(constants.TITLE)
        self.geometry(f'{constants.WIDTH}x{constants.HEIGHT}')
        self.iconbitmap(os.path.join(constants.ICONS_PATH, TOP_LEVEL_ICON))
        self.homeFrame = HomeFrame(master=self)
        self.homeFrame.pack(anchor=CENTER, expand=True, fill=BOTH, pady=50, padx=50)
        self.mainloop()
