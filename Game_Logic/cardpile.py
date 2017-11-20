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

class Community_Chest(CardPile):
    """
    Subclass(CardPile): Community_Chest
    """
    def __init__(self, name, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, position)
    
    def display(self, gamer, data_dict, dice_result):
        pass

class Chance(CardPile):
    """
    Subclass(CardPile): Chance
    """
    def __init__(self, name, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, position)
    
    def display(self, gamer, data_dict, dice_result):
        pass
