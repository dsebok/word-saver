class Word:
    def __init__(self, content):
        self.id = "default"
        self.content = content
        self.quantity = 1

    def increaseQuantity(self):
        self.quantity += 1
