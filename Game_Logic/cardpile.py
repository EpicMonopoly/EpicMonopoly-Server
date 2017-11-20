import block
import random


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
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data_dict: 
            :param dice_result: 
        """
        chance_list = data_dict["chance_list"]
        length_change_list = len(chance_list)
        random_card = chance_list[random.randint(0, length_change_list)]
        random_card.play()


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
        chest_list = data_dict["chest_list"]
        length_chest_list = len(chest_list)
        random_card = chest_list[random.randint(0, length_chest_list)]
        random_card.play()
