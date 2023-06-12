from enum import Enum, auto
from tkinter import Text

from CTkMessagebox import CTkMessagebox
from PIL import Image

import customtkinter
from customtkinter import *

from app.components.ctk_scrollable_dropdown import CTkScrollableDropdown
from app.services.translation_service import TranslationService
from app.utilities import constants

DEFAULT_LANGUAGES = ['english', 'romanian', 'french']
OUTPUT_PLACEHOLDER = 'Translation'
INPUT_OPTIONS_PLACEHOLDER = 'New Input Language'
OUTPUT_OPTIONS_PLACEHOLDER = 'New Output Language'
DETECT = 'Detect language'
SWITCH_ICON = 'switch_button.png'
SWITCH_BUTTON_DISABLED_COLOR = '#6e7f91'


class State(Enum):
    NORMAL = auto()
    DETECTING = auto()


class HomeFrame(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__translationService = TranslationService()
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.__never_translated = True
        self.__detect_tab_name = DETECT
        self.__input_languages = DEFAULT_LANGUAGES
        self.__output_languages = DEFAULT_LANGUAGES[::-1]
        self.__all_languages = [language for language in self.__translationService.get_languages()]
        self.__state = State.NORMAL
        self.__new_language_options()
        self.__switch_button = CTkButton(self, text='', width=28, height=28, corner_radius=100,
                                         command=self.__switch_languages_button,
                                         image=CTkImage(Image.open(os.path.join(
                                             constants.ICONS_PATH, SWITCH_ICON)), size=(28, 28)))
        self.__switch_button.grid(row=0, column=0, columnspan=2, sticky='s')
        self.__tabviews()
        self.__text_widgets()

        CTkButton(self, text='Translate', width=200, height=40, corner_radius=50, font=CTkFont('Arial', 18),
                  command=self.__translate)\
            .grid(row=2, column=0, columnspan=2, pady=25)

    def __new_language_options(self):
        self.__input_options = CTkComboBox(self, width=160)
        self.__input_options.grid(row=0, column=0, sticky='w', pady=15, padx=15)
        CTkScrollableDropdown(self.__input_options, values=self.__all_languages,
                              autocomplete=True, command=self.__select_new_input_language)
        self.__input_options.set(INPUT_OPTIONS_PLACEHOLDER)
        self.__input_options.bind('<Button>', command=lambda e: self.__input_options.set(''))

        self.__output_options = CTkComboBox(self, width=170)
        self.__output_options.grid(row=0, column=1, sticky='e', pady=15, padx=15)
        CTkScrollableDropdown(self.__output_options, values=self.__all_languages,
                              autocomplete=True, command=self.__select_new_output_language)
        self.__output_options.set(OUTPUT_OPTIONS_PLACEHOLDER)
        self.__output_options.bind('<Button>', command=lambda e: self.__output_options.set(''))

    def __tabviews(self):
        self.__input_tabview = customtkinter.CTkTabview(self, command=self.__input_tabview_command)
        self.__input_tabview.grid(row=1, column=0, sticky='nsew', padx=25)
        self.__input_tabview.add(self.__detect_tab_name)
        for language in self.__input_languages:
            self.__input_tabview.add(language)
        self.__input_tabview.set(self.__input_languages[0])

        self.__output_tabview = customtkinter.CTkTabview(self, command=self.__output_tabview_command)
        self.__output_tabview.grid(row=1, column=1, sticky='nsew', padx=25)
        for language in self.__output_languages:
            self.__output_tabview.add(language)

    def __text_widgets(self):
        self.__input_text = Text(self.__input_tabview, background='#343638', border=0,
                                 font=CTkFont('Arial', 22), foreground='white')
        self.__input_text.grid()

        self.__output_text = Text(self.__output_tabview, background='#303234', border=0,
                                  font=CTkFont('Arial', 22), foreground='gray')
        self.__output_text.insert(1.0, OUTPUT_PLACEHOLDER)
        self.__output_text.config(state='disabled')
        self.__output_text.grid()

    def __select_new_input_language(self, text):
        self.__input_options.set(INPUT_OPTIONS_PLACEHOLDER)
        self.__select_new_language(text, self.__input_tabview, self.__input_languages, 1)
        self.__input_tabview_command()

    def __select_new_output_language(self, text):
        self.__output_options.set(OUTPUT_OPTIONS_PLACEHOLDER)
        self.__select_new_language(text, self.__output_tabview, self.__output_languages)
        self.__output_tabview_command()

    def __select_new_language(self, text, tabview, languages, offset=0):
        self.focus()
        if text in languages:
            tabview.set(text)
            return
        if self.__state == State.DETECTING:
            tabview.set(languages[0])
        currentLanguage = tabview.get()
        currentIndex = languages.index(currentLanguage)
        tabview.delete(currentLanguage)
        tabview.insert(currentIndex + offset, text)
        tabview.set(text)
        languages[currentIndex] = text

    def __input_tabview_command(self):
        text = self.__input_text.get(1.0, 'end')
        if self.__input_tabview.get() not in self.__input_languages:
            self.__state = State.DETECTING
            print(self.__switch_button.cget('fg_color'))
            self.__switch_button.configure(state='disabled', fg_color=SWITCH_BUTTON_DISABLED_COLOR)
            self.__detect_language(text)
        else:
            self.__state = State.NORMAL
            self.__switch_button.configure(state='normal', fg_color='#1f538d')
            self.__switch_tab_languages(self.__input_tabview, self.__output_tabview, self.__output_languages)
        if len(text) > 1:
            self.__translate()

    def __output_tabview_command(self):
        self.__switch_tab_languages(self.__output_tabview, self.__input_tabview, self.__input_languages)
        if len(self.__input_text.get(1.0, 'end')) > 1:
            self.__translate()

    def __detect_language(self, text):
        detection = self.__translationService.detect_language(text)
        if detection.confidence > 0:
            detectedLanguage = self.__translationService.get_language_by_code(detection.lang)
            self.__input_tabview.delete(self.__detect_tab_name)
            self.__detect_tab_name = f'{detectedLanguage} - Detected'
            self.__input_tabview.insert(0, self.__detect_tab_name)
            self.__input_tabview.set(self.__detect_tab_name)

    def __switch_languages_button(self):
        inputTab = self.__input_tabview.get()
        outputTab = self.__output_tabview.get()
        if inputTab == outputTab:
            return
        if inputTab not in self.__output_languages:
            index = self.__output_languages.index(outputTab)
            self.__output_languages[index] = inputTab
            self.__output_tabview.delete(outputTab)
            self.__output_tabview.insert(index, inputTab)
        self.__output_tabview.set(inputTab)
        if outputTab not in self.__input_languages:
            index = self.__input_languages.index(inputTab)
            self.__input_languages[index] = outputTab
            self.__input_tabview.delete(inputTab)
            self.__input_tabview.insert(index, outputTab)
        self.__input_tabview.set(outputTab)
        inputText = self.__input_text.get(1.0, 'end')
        outputText = self.__output_text.get(1.0, 'end')
        if len(inputText) < 1 or len(outputText) < 1 or self.__never_translated:
            return
        self.__input_text.delete(1.0, 'end')
        self.__input_text.insert(1.0, outputText)
        self.__translate()

    def __translate(self):
        self.__never_translated = False
        text = self.__input_text.get(1.0, 'end')
        if len(text) < 1 or text == '\n':
            CTkMessagebox(title="Missing Input", message="Please enter your input text for translating",
                          icon='warning', option_1='Ok')
            if self.__output_text.get(1.0, 'end') != OUTPUT_PLACEHOLDER:
                self.__output_text.config(state='normal')
                self.__output_text.delete(1.0, 'end')
                self.__output_text.insert(1.0, OUTPUT_PLACEHOLDER)
                self.__output_text.config(state='disabled')
            return
        if self.__state == State.DETECTING:
            self.__detect_language(text)
        source = self.__input_tabview.get() if \
            self.__state == State.NORMAL else \
            self.__input_tabview.get().split(' - ')[0]
        destination = self.__output_tabview.get()
        answer = self.__translationService.translate_from_to(text, source, destination)

        self.__output_text.config(state='normal')
        self.__output_text.delete(1.0, 'end')
        self.__output_text.insert(1.0, answer.text)
        self.__output_text.config(state='disabled')

    @staticmethod
    def __switch_tab_languages(tabview1, tabview2, languages):
        if tabview1.get() == tabview2.get():
            for language in languages:
                if tabview2.get() != language:
                    tabview2.set(language)
                    break
