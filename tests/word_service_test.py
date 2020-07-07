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

    def test_text_check_doesnt_accept_brackets(self):
        # GIVEN
        text = "[] abcde"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_doesnt_accept_quotation_marks(self):
        # GIVEN
        text = "\"abcde\" is a quote"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_doesnt_accept_plus_signs(self):
        # GIVEN
        text = "add + these + words + together"
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)

    def test_text_check_doesnt_accept_only_whitespace(self):
        # GIVEN
        text = "   "
        # WHEN
        result = word_service.text_has_invalid_characters(text)
        # THEN
        self.assertTrue(result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
