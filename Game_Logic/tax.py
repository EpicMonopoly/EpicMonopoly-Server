import block
import operation


class Tax(block.Block):
    """
    Tax class
    """

    def __init__(self, name, block_id, position, rate):
        super().__init__(name, block_id, position)
        self._rate = rate

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    def display(self, gamer, data, dice_result):
        pass

    def change_value(self, new_rate):
        self._rate = self._rate * (1 + new_rate)


class Income_Tax(Tax):
    """
    Subclass(Tax): Income_Tax
    """

    def __init__(self, name, block_id, position, rate):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position, rate)

    def display(self, gamer, data, dice_result):
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data: 
            :param dice_result: 
        """
        bank = data['epic_bank']
        payment = gamer.cash * self.rate
        operation.pay(gamer, bank, payment, data)
        operation.push2all("%s pay %d for tax" % (gamer.name, payment))


class Super_Tax(Tax):
    """
    Subclass(Tax): Super_Tax
    """

    def __init__(self, name, block_id, position, rate):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, block_id, position, rate)

    def display(self, gamer, data, dice_result):
        """
        docstring here
            :type gamer: player.Player
            :param gamer: 
            :param data: 
            :param dice_result: 
        """
        bank = data['epic_bank']
        payment = gamer.calculate_asset_value() * self.rate
        operation.pay(gamer, bank, payment, data)
        operation.push2all("%s pay %d for tax" % (gamer.name, payment))
