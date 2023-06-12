from tkinter import Text

from customtkinter import *

import constants
from services.translation_service import TranslationService


class HomeFrame(CTkFrame):
    def __init__(self, master: CTk, **kwargs):
        super().__init__(master, **kwargs)
        self.translationService = TranslationService()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.inputText = Text(self, background='#343638', border=0, font=('Arial', 24), foreground='white')
        self.inputText.grid(row=0, column=0, sticky='nsew', padx=50, pady=50)

        self.outputText = Text(self, background='#343638', border=0, font=('Arial', 24), foreground='gray')
        self.outputText.insert(1.0, constants.OUTPUT_PLACEHOLDER)
        self.outputText.config(state='disabled')
        self.outputText.grid(row=0, column=1, padx=50, pady=50, ipadx=10, ipady=10, sticky='nsew')

        # temporary submit button
        CTkButton(self, text='Submit', command=self.submit) \
            .grid(row=1, column=0, columnspan=2, pady=30)

    def submit(self):
        text = self.inputText.get(1.0, 'end')
        src = 'ro'
        dest = 'en'
        answer = self.translationService.translate_from_to(text, src, dest)

        self.outputText.config(state='normal')
        self.outputText.delete(1.0, 'end')
        self.outputText.insert(1.0, answer.text)
        self.outputText.config(state='disabled')
