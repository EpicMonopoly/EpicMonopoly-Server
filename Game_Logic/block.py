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

    def getJSon_block(self):
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
        }
        return json_data


class Go(Block):
    """
    Subclass(Block): Go
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)
        self._description = description
        self._reward_value = 200

    @property
    def reward(self):
        return self._reward_value

    def display(self, gamer, data, dice_result):
        # import operation
        operation.pay(data['epic_bank'], gamer, self._reward_value, data)

    def change_value(self, rate):
        self._reward_value = self._reward_value * (1 + rate)
        print("Update reward to %d" % self._reward_value)

    def getJSon(self):
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
            "reward_value": self._reward_value
        }
        return json_data


class Go_To_Jail(Block):
    """
    Subclass(Block): Go_To_Jail
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)
        self._description = description

    def display(self, gamer, data, dice_result):
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data: 
            :param dice_result: 
        """
        data["msg"].push2single(gamer.id, operation.gen_hint_json("Move to jail"))
        gamer.move(steps=0, position=10)
        gamer.add_in_jail_time()
        gamer.cur_status = 0

    def change_value(self, rate):
        pass


class In_Jail(Block):
    """
    Subclass(Block): In_jail
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position)
        self._description = description
        self._bail_fee = 50

    def bail_fee(self, time):
        return self._bail_fee * time

    def display(self, gamer, data, dice_result):
        pass

    def change_value(self, rate):
        self._bail_fee = self._bail_fee * (1 + rate)


class Free_Parking(Block):
    """
    Subclass(Block): Free_Parking
    """

    def __init__(self, name, block_id, position, description):
        """
        Constructor 
        :param name: string
        :param position: int
        """
        super().__init__(name, block_id, position)
        self._description = description

    def display(self, gamer, data, dice_result):
        pass

    def change_value(self, rate):
        pass
