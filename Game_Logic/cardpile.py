from block import Block


class CardPile(Block):
    """
    CardPile class
    """
    def __init__(self):
        super().__init__()
        self._cards = []

    def append_card(self, card):
        self._cards.append(card)

    def pop_card(self):
        return self._cards.pop()

    def display(self):
        pass
