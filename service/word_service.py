from dao import mysql_dao


def getWordCount(word):
    quantity = mysql_dao.getWordCount(word)
    if quantity:
        return quantity[0]
    else:
        return 0


def getWordTable():
    return mysql_dao.getWordTable()
