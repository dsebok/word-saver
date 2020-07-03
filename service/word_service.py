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

def textHasInvalidCharacters(text):
    if text.strip()=="":
        return True
    text = re.sub(r"[ -:()?!,.\d]", "a", text)
    return not text.isalpha()
