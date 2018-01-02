import random


class Street:
    """
    Street class is a struct that contain 1-3 blocks
    """

    def __init__(self, street_id, color=None, block_list=None):
        """
        Construct method for Street
        :param color: color for this street
        :param block_list: block list
        """
        self._street_id = street_id
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def block_list(self):
        return self._block_list

    @block_list.setter
    def block_list(self, block_list):
        self._block_list = block_list

    def resort(self):
        """
        Shuffle the position of blocks
        """
        temp_list = []
        for block in self._block_list:
            temp_list.append(block.position())
        random.shuffle(self._block_list)
        for block in self._block_list:
            block.position(temp_list.pop())

    def getJSon(self):
        json_data = {
            "id": self._street_id,
            "color": self._color
        }
        return json_data
