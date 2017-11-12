from property import Property

class estate(Property):
    """
    Class estate
    """
    def __init__(self, value):
        """
        Call for superclass construct
        Init _houseNum and _houseValue
        :param value: The value of single house
        """
        super().__init__()
        self._houseNum = 0
        self._houseValue = value

    @property
    def value(self):
        return self._estate_value + (self._houseNum * self._houseValue)

    @property
    def mortgage_value(self):
        return self.value * self.mortgage_rate

