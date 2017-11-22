import block
import random


class CardPile(block.Block):
    """
    CardPile class
    """

    def __init__(self, name, block_id, position):
        super().__init__(name, block_id, position)
        self._cards = []

    def append_card(self, card):
        self._cards.append(card)

    def pop_card(self):
        return self._cards.pop()

    def display(self, gamer, data, dice_result):
        pass


class Community_Chest(CardPile):
    """
    Subclass(CardPile): Community_Chest
    """

    def __init__(self, name, block_id, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)

    def display(self, gamer, data, dice_result):
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data: 
            :param dice_result: 
        """
        chance_list = data["chance_list"]
        length_change_list = len(chance_list)
        random_card = chance_list[random.randint(0, length_change_list)]
        random_card.play(gamer, data)


class Chance(CardPile):
    """
    Subclass(CardPile): Chance
    """

    def __init__(self, name, block_id, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)

    def display(self, gamer, data, dice_result):
        chest_list = data["chest_list"]
        length_chest_list = len(chest_list)
        random_card = chest_list[random.randint(0, length_chest_list)]
        random_card.play(gamer, data)
