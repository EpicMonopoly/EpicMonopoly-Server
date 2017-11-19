import role
import player
import station
import utility
import estate


class Bank(role.Role):
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
        self._loan_list = []
        self._cur_house = 32
        self._cur_hotel = 12

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
        :type from_role: Role
        :type properties: set
        :param from_role: player
        :param properties: a set of properties
        :return: True or not of this mortgage
        """
        mortgage_value = 0
        if properties:
            for p in properties:
                if isinstance(p, station.Station):
                    mortgage_value += p.mortgage_value
                    self._loan_list.append(p)
                elif isinstance(p, utility.Utility):
                    mortgage_value += p.mortgage_value
                    self._loan_list.append(p)
                elif isinstance(p, estate.Estate):
                    mortgage_value += p.mortgage_value
                    self._loan_list.append(p)
            from_role.cash(mortgage_value)
            return True
        else:
            return False

    def repayment(self, from_role, properties):
        """
        Repay the mortgaged properties
        :type from_role: Role
        :type properties: set
        :param from_role: player
        :param properties: a set of properties
        :return: True or not of this repayment
        """
        repay_value = 0
        if properties:
            for p in properties:
                if isinstance(p, station.Station):
                    repay_value += p.mortgage_value
                    self._loan_list.append(p)
                elif isinstance(p, utility.Utility):
                    repay_value += p.mortgage_value
                    self._loan_list.append(p)
                elif isinstance(p, estate.Estate):
                    repay_value += p.mortgage_value
                    self._loan_list.append(p)
            from_role.cash(repay_value)
            return True
        else:
            return False

    def build_house(self, from_to, estate, house_num):
        """
        Build house on estate
        :type from_to: Role
        :type estate: Estate
        :param from_to: Role
        :param estate: the estate player want to build houses on
        :param house_num: number of house the player want to build
        :return: True or not about the result
        """
        if from_to.cash >= estate.house_value * house_num:
            if estate.house_num + house_num <= 4:
                estate.house_num(estate.house_num + house_num)
            elif estate.house_num + house_num == 5:
                estate.house_num(0)
                estate.hotel_num(1)
            else:
                return False
            from_to.cash(-estate.house_value * estate.house_num)
            return True
        else:
            return False

    # def build_hotel(self, estate):
    #     """
    #     estate
    #     :param estate:
    #     :return:
    #     """

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
        :type to_role: player.Player
        :type amount: int
        :param amount: amount of cash to be traded
        :param to_role: Player who receive the cash
        :return boolean: Trade finished or error
        """
        to_role._cash(amount)
        return True
