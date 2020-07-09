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

    def test_user_name_check_accepts_letters_digits_hypens_and_underscores(self):
        # GIVEN
        user_name = "test_me-100_times"
        # WHEN
        result = word_service.check_user_name(user_name)
        # THEN
        self.assertTrue(result)

    def test_user_name_check_accepts_input_if_it_has_min_one_letter(self):
        # GIVEN
        user_name_ok = "t34"
        user_name_not_ok = "134"
        # WHEN
        accepted_result = word_service.check_user_name(user_name_ok)
        denied_result = word_service.check_user_name(user_name_not_ok)
        # THEN
        self.assertTrue(accepted_result)
        self.assertFalse(denied_result)

    def test_user_name_check_denies_spaces(self):
        # GIVEN
        user_name = "test me"
        # WHEN
        result = word_service.check_user_name(user_name)
        # THEN
        self.assertFalse(result)

    def test_user_name_check_denies_less_than_3_chars(self):
        # GIVEN
        user_name = "me"
        # WHEN
        result = word_service.check_user_name(user_name)
        # THEN
        self.assertFalse(result)

    def test_user_name_check_denies_more_than_20_chars(self):
        # GIVEN
        user_name = "12345678901234567890a"
        # WHEN
        result = word_service.check_user_name(user_name)
        # THEN
        self.assertFalse(result)

    def test_user_name_check_denies_other_operators(self):
        # GIVEN
        user_name_plus = "abc+def"
        user_name_div = "abc/def"
        user_name_mult = "abc*def"
        user_name_mod = "abc\%def"
        # WHEN
        result_plus = word_service.check_user_name(user_name_plus)
        result_div = word_service.check_user_name(user_name_div)
        result_mult = word_service.check_user_name(user_name_mult)
        result_mod = word_service.check_user_name(user_name_mod)
        # THEN
        self.assertFalse(result_plus)
        self.assertFalse(result_div)
        self.assertFalse(result_mult)
        self.assertFalse(result_mod)

    def test_user_name_check_denies_any_parenthesis(self):
        #GIVEN
        user_name_parenth = "(name)"
        user_name_square = "[name]"
        user_name_curly = "{name}"
        user_name_angle = "<name>"
        # WHEN
        result_parenth = word_service.check_user_name(user_name_parenth)
        result_square = word_service.check_user_name(user_name_square)
        result_curly = word_service.check_user_name(user_name_curly)
        result_angle = word_service.check_user_name(user_name_angle)
        # THEN
        self.assertFalse(result_parenth)
        self.assertFalse(result_square)
        self.assertFalse(result_curly)
        self.assertFalse(result_angle)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
