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
    if text.strip() == "":
        return True
    text = re.sub(r"[ -:()?!,.\d]", "a", text)
    return not text.isalpha()


def saveText(text):
    wordList = convertToWordList(text)
    uniqueWordList = groupWords(wordList)  # this
    databaseList = getWordTable()
    newWordList = selectNewWords(wordList, databaseList)
    updateList = selectExistingWords(wordList, databaseList)
    mergedList = newWordList + updateList
    mysql_dao.updateWordTable(mergedList)


def convertToWordList(text):
    text = re.sub(r"[-:()?!,.\d]", "", text)
    return text.split()


def groupWords(wordList):
    return 0


def selectNewWords(wordList, databaseList):
    return 0


def selectExistingWords(wordList, databaseList):
    return 0
