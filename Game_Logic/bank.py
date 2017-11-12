from role import Role
from player import Player


class Bank(Role):
    """
    subclass(Role): Bank
    """

    def __init__(self, uid, name):
        """
        Constructor
        loan_list: set
        cur_house: int
        cur_hotel: int
        """
        super().__init__(uid, name, 0)
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

    def mortgage(self, from_role, properties):
        """
        Mortgage the properties of Player
        :type from_role: Player
        :type properties: set
        :param from_role: player
        :param properties: a set of properties
        :return:
        """
        # mortgage_value = 0
        # for p in properties:
        #     if isinstance(p, Station):
        pass

    def repayment(self):
        pass

    def build_house(self):
        pass

    def build_hotel(self):
        pass

    def trade_property(self, properties, from_role, to_role):
        """
        Trade for other players or bank, here is just to sell
        :type properties: set
        :type from_role: Bank
        :type to_role: Player
        :param properties: a set of Property
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade successfully or not
        """
        from_role.remove_property(properties)
        to_role.add_property(properties)
        return True

    def pay(self, amount, to_role):
        """
        Trade cash between players or bank
        :type to_role: Player
        :param amount: amount of cash to be traded
        :param to_role: Player who receive the cash
        :return boolean: Trade finished or error
        """
        to_role._cash(amount)
        return True
