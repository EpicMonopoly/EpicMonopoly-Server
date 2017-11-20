from property import Property
from ef import EF


class Estate(Property):
    """
    Class estate
    """
    def __init__(self, name, position, uid, estate_value, status, street_id, house_value):
        """
        Call for superclass construct
        Init _houseNum and _houseValue
        :param house_value: The value of single house
        """
        super().__init__(name, position, uid, estate_value, status)
        self._street_id = street_id
        self._house_num = 0
        self._house_value = house_value
        self._hotel_num = 0
        self._hotel_value = 4 * house_value

    @property
    def house_num(self):
        return self._house_num

    @house_num.setter
    def house_num(self, house_num):
        self._house_num = house_num

    @property
    def house_value(self):
        return self._house_value

    @property
    def hotel_num(self):
        return self._hotel_num

    @hotel_num.setter
    def hotel_num(self, hotel_num=1):
        if self._hotel_num == 0 and hotel_num == 1:
            self._hotel_num += hotel_num

    @property
    def value(self):
        return self._estate_value + (self._house_num * self._house_value)

    @property
    def mortgage_value(self):
        return self.value * self.mortgage_rate
      
    @property
    def payment(self):
        return self.value

    # TODO: implement the method
    # def change_house_value(self, EF):
    #     """
    #     Change house value according to EF
    #     :type EF: float
    #     :param EF: economy factor
    #     :return: None
    #     """

    # TODO: implementation this abstract method
    def display(self):
        """
        Display description
        :return:
        """
        pass
