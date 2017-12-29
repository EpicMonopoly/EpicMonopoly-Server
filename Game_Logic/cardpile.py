import block
import random


class CardPile(block.Block):
    """
    CardPile class
    """

    def __init__(self, name, block_id, position, description):
        super().__init__(name, block_id, position)
        self._cards = []
        self._description = description

    def append_card(self, card):
        self._cards.append(card)

    def pop_card(self):
        return self._cards.pop()

    def display(self, gamer, data, dice_result):
        pass

    def change_value(self, rate):
        for card in self._cards:
            card.change_value(rate)

    def getJSon(self):
        json_data = {
            "name": self._name,
            "position": self._position,
            "block_id": self._block_id,
            "description": self._description
        }
        return json_data


class Community_Chest(CardPile):
    """
    Subclass(CardPile): Community_Chest
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position, description)

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
        random_card = chance_list[random.randint(0, length_change_list - 1)]
        random_card.play(gamer, data)


class Chance(CardPile):
    """
    Subclass(CardPile): Chance
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position, description)

    def display(self, gamer, data, dice_result):
        chest_list = data["chest_list"]
        length_chest_list = len(chest_list)
        random_card = chest_list[random.randint(0, length_chest_list)]
        random_card.play(gamer, data)
