import role


class Bank(role):
    """
    subclass(Role): Bank
    """

    def __init__(self, uid, name, cash):
        """
        Constructor
        loan_list: set
        cur_house: int
        cur_hotel: int
        """
        super().__init__(uid, name, cash)
        self._loan_list = set()
        self._cur_house = int()
        self._cur_hotel = int()

    @property
    def loan_list(self):
        return self._loan_list

    @property
    def cur_house(self):
        return self._cur_house

    @property
    def cur_hotel(self):
        return self._cur_hotel

    def mortgage(self):
        pass

    def repayment(self):
        pass

    def build_house(self):
        pass

    def build_hotel(self):
        pass

    # TODO: implement method
    def trade_property(self, properties, from_role, to_role):
        """
        Treade for other players or bank
        :param properties: Property
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade successfully or not
        """
        pass

    # TODO: implement method
    def pay(self, amount, from_role, to_role):
        """
        Trade cash between players or bank
        :param amount: amount of cash to be traded
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade finished or error
        """
        pass