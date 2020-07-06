from .word import Word


class WordTable:

    def __init__(self):
        self.table = []

    def add(self, word):
        self.table.append(word)

    def contains_word(self, external_word):
        for word in self.table:
            if external_word.content.casefold() == word.content.casefold():
                return True
        return False

    def increase_quantity(self, external_word):
        for word in self.table:
            if external_word.content.casefold() == word.content.casefold():
                word.increase_quantity()

    def get_word(self, content):
        for word in self.table:
            if content.casefold() == word.content.casefold():
                return word
        return Word()
