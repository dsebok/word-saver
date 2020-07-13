from dao import mysql_dao
from domain.word import Word
from domain.word_table import WordTable
from transformers import word_table_transformer
import re

_GENERAL_EMAIL_REGEX = r"^[a-z0-9]+[a-z0-9_\.+-]*[a-z0-9]+\@([a-z0-9-]+\.)+[a-z0-9]+$"


def get_word_count(word):
    quantity = mysql_dao.get_word_count(word)
    if quantity:
        return quantity[0]
    else:
        return 0


def get_word_table():
    return mysql_dao.get_word_table()


def word_has_invalid_characters(word):
    word = re.sub(r"[\d]", "a", word)
    return not word.isalpha()


def text_has_invalid_characters(text):
    if text.strip() == "":
        return True
    text = re.sub(r"[\*\"+%/]", "=", text)
    text = re.sub(r"[ '-:()?!,.\d]", "", text)
    text += "a"
    return not text.isalpha()


def save_text(text):
    db_list = get_word_table()
    db_table = word_table_transformer.transform_db_list_to_word_table(db_list)
    word_table = word_table_transformer.transform_text_to_word_table(text)
    new_word_table = _select_new_words(word_table, db_table)
    update_table = _select_existing_words(word_table, db_table)
    new_word_list = word_table_transformer.transform_word_table_to_db_list(new_word_table)
    update_list = word_table_transformer.transform_word_table_to_db_list(update_table)
    merged_list = new_word_list + update_list
    mysql_dao.update_word_table(merged_list)


def check_user_name(user_name):
    user_name = user_name.strip()
    if len(user_name) < 3 or len(user_name) > 20:
        return False
    user_name = re.sub(r"[\*\"+%/]", "=", user_name)
    user_name = re.sub(r"[-_\d]", "", user_name)
    return user_name.isalpha()


def check_password(password):
    password = password.strip()
    if len(password) < 8 or len(password) > 20:
        return False
    contains_lower_case = bool(re.search(r"[a-z]", password))
    contains_upper_case = bool(re.search(r"[A-Z]", password))
    contains_min_two_digits = _check_digits_in_pwd(password)
    if contains_lower_case and contains_upper_case and contains_min_two_digits:
        return _contains_special_char(password)
    return False


def confirm_password(password, confirmed_pwd):
    return password == confirmed_pwd
    

def check_email(email):
    return bool(re.match(_GENERAL_EMAIL_REGEX, email))


def check_email_in_db(email):
    user_found = mysql_dao.get_user_info(email)
    if user_found:
        return False
    return True


def _select_new_words(word_table, db_table):
    new_word_table = WordTable()
    for word in word_table.table:
        if not db_table.contains_word(word):
            new_word_table.add(word)
    return new_word_table


def _select_existing_words(word_table, db_table):
    update_table = WordTable()
    for word in word_table.table:
        if db_table.contains_word(word):
            db_word = db_table.get_word(word.content)
            word.quantity += db_word.quantity
            word.id = db_word.id
            update_table.add(word)
    return update_table


def _check_digits_in_pwd(pwd):
    count = 0
    while len(pwd) > 0:
        if pwd[0].isdigit():
            count += 1
        pwd = pwd[1:]
    return count > 1


def _contains_special_char(pwd):
    pwd = re.sub(r"[ a-zA-Z\d]", "", pwd)
    return len(pwd) > 0