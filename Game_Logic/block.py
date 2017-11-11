from abc import ABCMeta, abstractclassmethod


class Block(metaclass=ABCMeta):
    """
    Abstract class: Block
    """

    def __init__(self):
        """
        Constructor
        initialize variable:
        name: string
        position: int
        """
        self._name = str()
        self._position = int()

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @abstractclassmethod
    def display(self):
        pass
