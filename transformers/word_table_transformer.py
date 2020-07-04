from domain.word import Word
from domain.word_table import WordTable


def transformTextToWordTable(text):

    return 0


def transformDbListToWordTable():
    return 0


def transformWordTableToDbList():
    return 0


def convertToWordList(text):
    text = re.sub(r"[-:()?!,.\d]", "", text)
    return text.split()


def groupWords(wordList):
    uniqueWordList = []
    for word in wordList:
        #    if alreadyInList
