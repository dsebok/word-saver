from dao import mysql_dao
import re


def getWordCount(word):
    quantity = mysql_dao.getWordCount(word)
    if quantity:
        return quantity[0]
    else:
        return 0


def getWordTable():
    return mysql_dao.getWordTable()


def textIsNotAlphabetical(text):
    text = text.replace(" ", "")
    text = re.sub(r"[-:()?!,.\d]", "", text)
    return not text.isalpha()
