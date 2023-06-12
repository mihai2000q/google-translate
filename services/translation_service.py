import googletrans
from googletrans import Translator


class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_from_to(self, text, src, dest):
        s = googletrans.LANGCODES[src.lower()]
        d = googletrans.LANGCODES[dest.lower()]
        return self.translator.translate(text=text, src=s, dest=d)

    def detect_language(self, text):
        return self.translator.detect(text=text)

    @staticmethod
    def get_languages():
        return list(googletrans.LANGUAGES.values())
