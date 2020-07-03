import sys
sys.path.append("d:\\Code_Life\\repos\\VSCodeProjects\\WordSaver")
from service import word_service
import unittest


class WordServiceTest(unittest.TestCase):
    def test_word_check_accepts_letters(self):
        # GIVEN
        word = "abcdefgh"
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_accepts_digits(self):
        # GIVEN
        word = "1234567890"
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_accepts_certain_punctuations(self):
        # GIVEN
        word = "-:()?!,."
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertFalse(result)


    def test_word_check_accepts_space_and_combined_characters(self):
        # GIVEN
        word = "What is life? How could someone so talented die so young?! What is being young?"
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertFalse(result)

    def test_word_check_doesnt_accept_other_punctuations(self):
        # GIVEN
        word = "[]'abcde()"
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertTrue(result)

    def test_word_check_doesnt_accept_only_whitespace(self):
        # GIVEN
        word = "   "
        # WHEN
        result = word_service.textHasInvalidCharacters(word)
        # THEN
        self.assertTrue(result)

def main():
    unittest.main()


if __name__ == "__main__":
    main()
