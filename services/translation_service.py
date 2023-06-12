import googletrans
from googletrans import Translator


class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_from_to(self, text, src, dest):
        return self.translator.translate(text=text, src=src, dest=dest)

    def detect_language(self, text):
        return self.translator.detect(text=text)

    @staticmethod
    def get_languages():
        return googletrans.LANGUAGES

    @staticmethod
    def get_language_codes():
        return googletrans.LANGCODES
