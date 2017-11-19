import block


class Tax(block.Block):
    def __init__(self, rate):
        super().__init__()
        self._rate = rate

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    def display(self):
        pass
