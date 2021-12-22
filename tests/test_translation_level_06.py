import hedy
from test_level_01 import HedyTester
import hedy_translation

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel6(HedyTester):
    level = 6
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_multiplication(self):
        code = "vermenigvuldiging is 3 * 8"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "vermenigvuldiging is 3 * 8"

        self.assertEqual(expected, result)

    def test_addition(self):
        code = "print 'Hallo welkom bij Hedy' 5 + 7"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 'Hallo welkom bij Hedy' 5 + 7"

        self.assertEqual(expected, result)

    def test_division_dutch_english(self):
        code = "angle is 360 / angles"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "angle is 360 / angles"

        self.assertEqual(expected, result)

    def test_division_with_equals_dutch_english(self):
        code = "angle is 360 / angles"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "angle = 360 / angles"

        self.assertEqual(expected, result)

    def test_translate_back(self):
        code ="breuk is 13 / 4"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)