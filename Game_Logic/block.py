from abc import ABCMeta, abstractclassmethod
import operation


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
        return self._name

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

    @abstractclassmethod
    def display(self, gamer, data, dice_result):
        pass

    @abstractclassmethod
    def change_value(self, rate):
        pass


class Go(Block):
    """
    Subclass(Block): Go
    """

    def __init__(self, name, block_id, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)
        self.reward_value = 200

    def display(self, gamer, data, dice_result):
        # import operation
        operation.pay(data['epic_bank'], gamer, self.reward_value, data)
    
    def change_value(self, rate):
        pass


class Go_To_Jail(Block):
    """
    Subclass(Block): Go_To_Jail
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
        operation.push2all("Move to Jail")
        gamer.move(steps=0, position=10)
        gamer.cur_status = 0


class In_Jail(Block):
    """
    Subclass(Block): In_jail
    """

    def __init__(self, name, block_id, position):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)
        self._bail_fee = 50

    @property
    def bail_fee(self):
        return self._bail_fee

    def display(self, gamer, data, dice_result):
        pass


class Free_Parking(Block):
    """
    Subclass(Block): Free_Parking
    """

    def __init__(self, name, block_id, position):
        """
        Constructor 
        :param name: string
        :param position: int
        """
        super().__init__(name, block_id, position)

    def display(self, gamer, data, dice_result):
        pass
