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
        user_name_mod = r"abc\%def"
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
        # GIVEN
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

    def test_password_check_accepts_any_chars(self):
        # GIVEN
        pwd = "tst_ME 123-+!%/=(˘\'"
        # WHEN
        result = word_service.check_password(pwd)
        # THEN
        self.assertTrue(result)

    def test_password_check_denies_only_spaces(self):
        # GIVEN
        pwd = "      "
        # WHEN
        result = word_service.check_password(pwd)
        # THEN
        self.assertFalse(result)

    def test_password_check_requires_min_8_chars(self):
        # GIVEN
        pwd_ok = "tME1234*"
        pwd_denied = "tME123*"
        # WHEN
        result_ok = word_service.check_password(pwd_ok)
        result_denied = word_service.check_password(pwd_denied)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied)

    def test_password_check_accepts_max_20_chars(self):
        # GIVEN
        pwd_ok = "test_ME-901234567890"
        pwd_denied = "test_ME-9012345678901"
        # WHEN
        result_ok = word_service.check_password(pwd_ok)
        result_denied = word_service.check_password(pwd_denied)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied)

    def test_password_check_requires_1_lowercase_letter(self):
        # GIVEN
        pwd_ok = "testME_now24"
        pwd_denied = "TESTME_NOW24"
        # WHEN
        result_ok = word_service.check_password(pwd_ok)
        result_denied = word_service.check_password(pwd_denied)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied)

    def test_password_check_requires_1_uppercase_letter(self):
        # GIVEN
        pwd_ok = "testME_now24"
        pwd_denied = "testme_now24"
        # WHEN
        result_ok = word_service.check_password(pwd_ok)
        result_denied = word_service.check_password(pwd_denied)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied)

    def test_password_check_requires_2_digits(self):
        # GIVEN
        pwd_ok = "testME_now24"
        pwd_denied = "testME_now2"
        # WHEN
        result_ok = word_service.check_password(pwd_ok)
        result_denied = word_service.check_password(pwd_denied)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied)

    def test_password_check_requires_1_special_char(self):
        # GIVEN
        pwd_ok_1 = "testME_now24"
        pwd_ok_2 = "testME*now24"
        pwd_ok_3 = "testME%now24"
        pwd_ok_4 = "testME}now24"
        pwd_ok_5 = "testME^now24"
        pwd_denied_1 = "testMEnow24"
        pwd_denied_2 = "testME now24"
        # WHEN
        result_ok_1 = word_service.check_password(pwd_ok_1)
        result_ok_2 = word_service.check_password(pwd_ok_2)
        result_ok_3 = word_service.check_password(pwd_ok_3)
        result_ok_4 = word_service.check_password(pwd_ok_4)
        result_ok_5 = word_service.check_password(pwd_ok_5)
        result_denied_1 = word_service.check_password(pwd_denied_1)
        result_denied_2 = word_service.check_password(pwd_denied_2)
        # THEN
        self.assertTrue(result_ok_1)
        self.assertTrue(result_ok_2)
        self.assertTrue(result_ok_3)
        self.assertTrue(result_ok_4)
        self.assertTrue(result_ok_5)
        self.assertFalse(result_denied_1)
        self.assertFalse(result_denied_2)

    def test_email_check_accepts_normal_email_address(self):
        # GIVEN
        email_1 = "test@normal.com"
        email_2 = "te_st@normal.com"
        email_3 = "te-st@normal.com"
        email_4 = "te+st@normal.com"
        # WHEN
        result_1 = word_service.check_email(email_1)
        result_2 = word_service.check_email(email_2)
        result_3 = word_service.check_email(email_3)
        result_4 = word_service.check_email(email_4)
        # THEN
        self.assertTrue(result_1)
        self.assertTrue(result_2)
        self.assertTrue(result_3)
        self.assertTrue(result_4)

    def test_email_check_requires_point_after_at(self):
        # GIVEN
        email = "te.st@normalcom"
        # WHEN
        result = word_service.check_email(email)
        # THEN
        self.assertFalse(result)

    def test_email_check_denies_point_in_special_places(self):
        # GIVEN
        email_ok = "test@normal.com"
        email_denied_1 = "test@.normal.com"
        email_denied_2 = "test@normal.com."
        email_denied_3 = "test@normal..com"
        # WHEN
        result_ok = word_service.check_email(email_ok)
        result_denied_1 = word_service.check_email(email_denied_1)
        result_denied_2 = word_service.check_email(email_denied_2)
        result_denied_3 = word_service.check_email(email_denied_3)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied_1)
        self.assertFalse(result_denied_2)
        self.assertFalse(result_denied_3)

    def test_email_check_accepts_only_1_at(self):
        # GIVEN
        email_ok = "test@normal.com"
        email_denied_1 = "testnormal.com"
        email_denied_2 = "test@norm@al.com"
        email_denied_3 = "test@normal.comtest@normal.com"
        # WHEN
        result_ok = word_service.check_email(email_ok)
        result_denied_1 = word_service.check_email(email_denied_1)
        result_denied_2 = word_service.check_email(email_denied_2)
        result_denied_3 = word_service.check_email(email_denied_3)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied_1)
        self.assertFalse(result_denied_2)
        self.assertFalse(result_denied_3)

    def test_email_check_denies_some_special_chars(self):
        # GIVEN
        email_ok = "te_st@normal.com"
        email_denied_1 = "te$st@normal.com"
        email_denied_2 = "te/st@normal.com"
        email_denied_3 = "te*st@normal.com"
        # WHEN
        result_ok = word_service.check_email(email_ok)
        result_denied_1 = word_service.check_email(email_denied_1)
        result_denied_2 = word_service.check_email(email_denied_2)
        result_denied_3 = word_service.check_email(email_denied_3)
        # THEN
        self.assertTrue(result_ok)
        self.assertFalse(result_denied_1)
        self.assertFalse(result_denied_2)
        self.assertFalse(result_denied_3)

    def test_confirm_password_accepts_matching_strings(self):
        # GIVEN
        pwd = "testMEl1keH3||"
        confirmed_pwd = "testMEl1keH3||"
        # WHEN
        result = word_service.confirm_password(pwd, confirmed_pwd)
        # THEN
        self.assertTrue(result)

    def test_confirm_password_denies_mismatching_strings(self):
        # GIVEN
        pwd = "testMEl1keH3||"
        confirmed_pwd = "testME25%"
        # WHEN
        result = word_service.confirm_password(pwd, confirmed_pwd)
        # THEN
        self.assertFalse(result)

    def test_confirm_password_is_case_sensitive(self):
        # GIVEN
        pwd = "testMEl1keH3||"
        confirmed_pwd = "TestMEl1keH3||"
        # WHEN
        result = word_service.confirm_password(pwd, confirmed_pwd)
        # THEN
        self.assertFalse(result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
