from tkinter import Text

import customtkinter
from customtkinter import *

import constants
from services.translation_service import TranslationService


class HomeFrame(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translationService = TranslationService()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.languages = constants.DEFAULT_LANGUAGES
        self.__tabviews()
        self.__text_widgets()

        CTkButton(self, text='Submit', command=self.__translate) \
            .grid(row=1, column=0, columnspan=2, pady=10)

    def __tabviews(self):
        self.input_tabview = customtkinter.CTkTabview(self, command=self.__input_tabview_command)
        self.input_tabview.grid(row=0, column=0, sticky='nsew', padx=25, pady=25)
        for language in self.languages:
            self.input_tabview.add(language)

        self.output_tabview = customtkinter.CTkTabview(self, command=self.__output_tabview_command)
        self.output_tabview.grid(row=0, column=1, sticky='nsew', padx=25, pady=25)
        for language in self.languages[::-1]:
            self.output_tabview.add(language)

    def __text_widgets(self):
        self.input_text = Text(self.input_tabview, background='#343638', border=0, font=('Arial', 24),
                               foreground='white')
        self.input_text.grid()

        # self.input_text.bind('<Key>', lambda event: self.__translate())

        self.output_text = Text(self.output_tabview, background='#343638', border=0, font=('Arial', 24),
                                foreground='gray')
        self.output_text.insert(1.0, constants.OUTPUT_PLACEHOLDER)
        self.output_text.config(state='disabled')
        self.output_text.grid()

    def __translate(self):
        text = self.input_text.get(1.0, 'end')
        if len(text) < 1 or text == '\n':
            return
        source = self.input_tabview.get()
        destination = self.output_tabview.get()
        answer = self.translationService.translate_from_to(text, source, destination)

        self.output_text.config(state='normal')
        self.output_text.delete(1.0, 'end')
        self.output_text.insert(1.0, answer.text)
        self.output_text.config(state='disabled')

    def __input_tabview_command(self):
        self.__switch_tab_languages(self.output_tabview, self.input_tabview)

    def __output_tabview_command(self):
        self.__switch_tab_languages(self.input_tabview, self.output_tabview)

    def __switch_tab_languages(self, tabview1, tabview2):
        if tabview1.get() == tabview2.get():
            for language in self.languages:
                if tabview1.get() != language:
                    tabview1.set(language)
                    break
