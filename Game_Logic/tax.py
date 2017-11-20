import block


class Tax(block.Block):
    """
    Tax class
    """
    def __init__(self, name, position, rate):
        super().__init__(name, position)
        self._rate = rate

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    # TODO: implement display
    def display(self):
        pass

class Income_Tax(Tax):
    """
    Subclass(Tax): Income_Tax
    """
    def __init__(self, name, position, rate):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, position, rate)
    
    def display(self, gamer, data_dict, dice_result):
        pass

class Super_Tax(Tax):
    """
    Subclass(Tax): Super_Tax
    """
    def __init__(self, name, position, rate):
        """
        Constructor 
            :param name: string
            :param position: int
        """
        super().__init__(name, position, rate)
    
    def display(self, gamer, data_dict, dice_result):
        pass
