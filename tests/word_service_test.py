import unittest
import sys
sys.path.append("d:\\Code_Life\\repos\\VSCodeProjects\\WordSaver")
from service import word_service


class WordServiceTest(unittest.TestCase):
    def test_text_check_accepts_letters(self):
        # GIVEN
        text = "abcdefgh"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertFalse(result)

    def test_text_check_accepts_digits(self):
        # GIVEN
        text = "1234567890"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertFalse(result)

    def test_text_check_accepts_certain_punctuations(self):
        # GIVEN
        text = "'-:()?!,."
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertFalse(result)

    def test_text_check_accepts_space_and_combined_characters(self):
        # GIVEN
        text = "What is life? How could someone so talented die so young?! What is being young?"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertFalse(result)

    def test_text_check_denies_brackets(self):
        # GIVEN
        text = "[] abcde"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_denies_quotation_marks(self):
        # GIVEN
        text = "\"abcde\" is a quote"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_denies_plus_signs(self):
        # GIVEN
        text = "add + these + words + together"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_denies_only_whitespace(self):
        # GIVEN
        text = "   "
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_denies_empty_char(self):
        # GIVEN
        text = ""
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_word_check_accepts_letters(self):
        # GIVEN
        word = "abcdefgh"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_accepts_capital_letters_as_well(self):
        # GIVEN
        word = "AbCdEfGh"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertFalse(result)
        
    def test_word_check_accepts_only_digits(self):
        # GIVEN
        word = "0123456789"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_accepts_digits_and_letters_combined(self):
        # GIVEN
        word = "A0d1fg2rg3Tgs4gdf5gg6g789xxx"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_denies_prespace(self):
        # GIVEN
        word = " prespace"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)
    
    def test_word_check_denies_midspace(self):
        # GIVEN
        word = "mid space"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)

    def test_word_check_denies_parenthesis(self):
        # GIVEN
        word = "(parenthesis)"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)

    def test_word_check_denies_hyphen(self):
        # GIVEN
        word = "hy-phen"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)

    def test_word_check_denies_comma(self):
        # GIVEN
        word = "comma,"
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)
    
    def test_word_check_denies_only_space(self):
        # GIVEN
        word = "   "
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)

    def test_word_check_denies_empty_char(self):
        # GIVEN
        word = ""
        # WHEN
        result = word_service.word_has_invalid_characters(word)
        # THEN
        self.assertTrue(result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
