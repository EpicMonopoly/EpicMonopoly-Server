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
