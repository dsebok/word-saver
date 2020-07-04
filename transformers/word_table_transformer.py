from domain.word import Word
from domain.word_table import WordTable
import re


def transformTextToWordTable(text):
    wordList = convertToWordList(text)
    wordTable = convertListToTable(wordList)
    return wordTable


def transformDbListToWordTable(dbList):
    wordTable = WordTable()
    for dbWord in dbList:
        word = Word(dbWord[1])
        word.id = dbWord[0]
        word.quantity = dbWord[2]
        wordTable.add(word)
    return wordTable


def transformWordTableToDbList(wordTable):
    dbList = []
    for word in wordTable.table:
        dbWord = [""] * 3
        dbWord[0] = word.id
        dbWord[1] = word.content
        dbWord[2] = word.quantity
        dbList.append(dbWord)
    return dbList


def convertToWordList(text):
    text = re.sub(r"[:()?!,.]", " ", text)
    text = re.sub(r"[-]", "", text)
    return text.split()


def convertListToTable(wordList):
    wordTable = WordTable()
    for content in wordList:
        word = Word(content)
        if wordTable.containsWord(word):
            wordTable.increaseQuantity(word)
        else:
            wordTable.add(word)
    return wordTable
