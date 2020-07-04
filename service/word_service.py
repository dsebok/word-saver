from dao import mysql_dao
from domain.word import Word
from domain.word_table import WordTable
from transformers import word_table_transformer
import re


def getWordCount(word):
    quantity = mysql_dao.getWordCount(word)
    if quantity:
        return quantity[0]
    else:
        return 0


def getWordTable():
    return mysql_dao.getWordTable()


def wordHasInvalidCharacters(word):
    if word.strip() == "":
        return True
    word = re.sub(r"[\d]", "a", word)
    return not word.isalpha()


def textHasInvalidCharacters(text):
    if text.strip() == "":
        return True
    text = re.sub(r"[\*\'\"+%/]", "=", text)    
    text = re.sub(r"[ -:()?!,.\d]", "", text)
    text += "a"
    return not text.isalpha()


def saveText(text):
    dbList = getWordTable()
    dbTable = word_table_transformer.transformDbListToWordTable(dbList)
    wordTable = word_table_transformer.transformTextToWordTable(text)
    newWordTable = selectNewWords(wordTable, dbTable)
    updateTable = selectExistingWords(wordTable, dbTable)
    newWordList = word_table_transformer.transformWordTableToDbList(newWordTable)
    updateList = word_table_transformer.transformWordTableToDbList(updateTable)
    mergedList = newWordList + updateList
    mysql_dao.updateWordTable(mergedList)


def selectNewWords(wordTable, dbTable):
    newWordTable = WordTable()
    for word in wordTable.table:
        if not dbTable.containsWord(word):
            newWordTable.add(word)
    return newWordTable


def selectExistingWords(wordTable, dbTable):
    updateTable = WordTable()
    for word in wordTable.table:
        if dbTable.containsWord(word):
            dbWord = dbTable.getWord(word.content)
            word.quantity += dbWord.quantity
            word.id = dbWord.id
            updateTable.add(word)
    return updateTable
