from dao import mysql_dao
from domain.word import Word
from domain.word_table import WordTable
from transformers import word_table_transformer
import re


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
    return True


def check_password(password):
    return True


def check_email(email):
    return True


def check_email_in_db(email):
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
