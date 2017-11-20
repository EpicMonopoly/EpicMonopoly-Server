from abc import ABCMeta, abstractclassmethod


class Block(metaclass=ABCMeta):
    """
    Abstract class: Block
    """

    def __init__(self, name, block_id, position):
        """
        Constructor
        initialize variable:
        name: string
        position: int
        """
        self._name = name
        self._block_id = block_id
        self._position = position

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def block_id(self):
        return self._block_id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

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
        import operation
        operation.pay(data_dict['epic_bank'], gamer, 200)


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
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data_dict: 
            :param dice_result: 
        """
        gamer.move(steps=0, position=10)
        gamer.cur_status(0)


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

