from unittest import TestCase

from app.services.translation_service import TranslationService


class TestTranslationService(TestCase):
    def setUp(self):
        self.uut = TranslationService()

    def test_translate_from_romanian_to_english(self):
        text = 'vreau sa te vad'
        source = 'romanian'
        destination = 'english'

        output = self.uut.translate_from_to(text, source, destination)

        expected = 'I want to see you'
        self.assertEqual(output.text, expected)

    def test_detect_language(self):
        input1 = 'Vreau sa te vad'
        input2 = 'I want to see you'
        input3 = 'Je dois aller chez mois'

        output1 = self.uut.detect_language(input1)
        output2 = self.uut.detect_language(input2)
        output3 = self.uut.detect_language(input3)

        self.assertEqual(output1.lang, 'ro')
        self.assertEqual(output2.lang, 'en')
        self.assertEqual(output3.lang, 'fr')
