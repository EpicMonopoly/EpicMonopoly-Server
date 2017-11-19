import block


class CardPile(block.Block):
    """
    CardPile class
    """
    def __init__(self, name, position):
        super().__init__(name, position)
        self._cards = []

    def append_card(self, card):
        self._cards.append(card)

    def pop_card(self):
        return self._cards.pop()

    # TODO: implement display
    def display(self):
        pass
