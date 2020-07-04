from .word import Word


class WordTable:

    def __init__(self):
        self.table = []

    def add(self, word):
        self.table.append(word)

    def containsWord(self, externalWord):
        for word in self.table:
            if externalWord.content.casefold() == word.content.casefold():
                return True
        return False

    def increaseQuantity(self, externalWord):
        for word in self.table:
            if externalWord.content.casefold() == word.content.casefold():
                word.increaseQuantity()

    def getWord(self, content):
        for word in self.table:
            if content.casefold() == word.content.casefold():
                return word
        return Word()
