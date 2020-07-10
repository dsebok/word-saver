from domain.word import Word
from domain.word_table import WordTable
import re


def transform_text_to_word_table(text):
    word_list = _convert_to_word_list(text)
    word_table = _convert_list_to_table(word_list)
    return word_table


def transform_db_list_to_word_table(db_list):
    word_table = WordTable()
    for db_word in db_list:
        word = Word(db_word[1])
        word.id = db_word[0]
        word.quantity = db_word[2]
        word_table.add(word)
    return word_table


def transform_word_table_to_db_list(word_table):
    db_list = []
    for word in word_table.table:
        db_word = [""] * 3
        db_word[0] = word.id
        db_word[1] = word.content
        db_word[2] = word.quantity
        db_list.append(db_word)
    return db_list


def _convert_to_word_list(text):
    text = text.lower()
    text = re.sub(r"[':()?!,.]", " ", text)
    text = re.sub(r"[-]", "", text)
    return text.split()


def _convert_list_to_table(word_list):
    word_table = WordTable()
    for content in word_list:
        word = Word(content)
        if word_table.contains_word(word):
            word_table.increase_quantity(word)
        else:
            word_table.add(word)
    return word_table
