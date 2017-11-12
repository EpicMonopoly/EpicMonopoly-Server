import block


class CardPile(block):
    def __init__(self):
        self._cards = []

    def append_card(self, card):
        self._cards.append(card)

    def pop_card(self):
        return self._cards.pop()

    def display(self):
        pass
