from abc import ABCMeta, abstractclassmethod


class Block(metaclass=ABCMeta):
    """
    Abstract class: Block
    """

    def __init__(self, name, position):
        """
        Constructor
        initialize variable:
        name: string
        position: int
        """
        self._name = name
        self._position = position

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
    def display(self, gamer, data_dict, dice_result):
        pass

class Go(Block):
    """
    Subclass(Block): Go
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

class Go_To_Jail(Block):
    """
    Subclass(Block): Go_To_Jail
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

class In_Jail(Block):
    """
    Subclass(Block): In_jail
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

class Free_Parking(Block):
    """
    Subclass(Block): Free_Parking
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
    
