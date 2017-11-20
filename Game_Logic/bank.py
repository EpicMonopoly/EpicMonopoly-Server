import role


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
        self._loan_dict = {}
        self._cur_house = 32
        self._cur_hotel = 12

    @property
    def loan_list(self):
        return self._loan_dict

    @property
    def cur_house(self):
        return self._cur_house

    @property
    def cur_hotel(self):
        return self._cur_hotel

    def built_house(self):
        self._cur_house = self.cur_house - 1
    
    def built_hotel(self):
        self._cur_hotel = self._cur_hotel - 1

    def remove_house(self, number):
        self._cur_house = self.cur_house + number
    
    def remove_hotel(self):
        self._cur_hotel = self._cur_hotel - 1

    def add_loan_dict(self, asset_id, amount):
        self._loan_dict
    
    def remove_loan_dict(self, asset_id):
        if asset_id in self._loan_dict.keys():
            del self._loan_dict[asset_id]

    # def mortgage(self, from_role, assets):
    #     """
    #     Mortgage the assets of Player
    #     :type from_role: player.Player
    #     :type assets: list
    #     :param from_role: player
    #     :param assets: a set of assets
    #     :return: True or not of this mortgage
    #     """
    #     import station
    #     import utility
    #     import estate
    #     mortgage_value = 0
    #     if assets:
    #         for asset in assets:
    #             if isinstance(asset, station.Station):
    #                 mortgage_value += asset.mortgage_value
    #                 self._loan_list.append(asset)
    #             elif isinstance(asset, utility.Utility):
    #                 mortgage_value += asset.mortgage_value
    #                 self._loan_list.append(asset)
    #             elif isinstance(asset, estate.Estate):
    #                 mortgage_value += asset.mortgage_value
    #                 self._loan_list.append(asset)
    #         from_role.cash(mortgage_value)
    #         return True
    #     else:
    #         return False

    def repayment(self, from_role, assets):
        """
        Repay the mortgaged assets
        :type from_role: player.Player
        :type assets: list
        :param from_role: player
        :param assets: a set of assets
        :return: True or not of this repayment
        """
        import station
        import utility
        import estate
        repay_value = 0
        if assets:
            for a in assets:
                if isinstance(a, station.Station):
                    repay_value += a.mortgage_value
                    self._loan_dict.append(a)
                elif isinstance(a, utility.Utility):
                    repay_value += a.mortgage_value
                    self._loan_dict.append(a)
                elif isinstance(a, estate.Estate):
                    repay_value += a.mortgage_value
                    self._loan_dict.append(a)
            from_role.cash(repay_value)
            return True
        else:
            return False

    # def build_house(self, from_to, estate, house_num):
    #     """
    #     Build house on estate
    #     :type from_to: player.Player
    #     :type estate: Estate
    #     :param from_to: player
    #     :param estate: the estate player want to build houses on
    #     :param house_num: number of house the player want to build
    #     :return: True or not about the result
    #     """
    #     if from_to.cash >= estate.house_value * house_num:
    #         if estate.house_num + house_num <= 4:
    #             estate.house_num(estate.house_num + house_num)
    #         elif estate.house_num + house_num == 5:
    #             estate.house_num(0)
    #             estate.hotel_num(1)
    #         else:
    #             return False
    #         from_to.cash(-estate.house_value * estate.house_num)
    #         return True
    #     else:
    #         return False

    # def build_hotel(self, estate):
    #     """
    #     estate
    #     :param estate:
    #     :return:
    #     """

    def add_asset(self, new_asset):
        """
        Add asset to player
        :type new_asset: estate.Estate, station.Station, utility.Utility
        :param self: self
        """
        import station
        import utility
        import estate
        if isinstance(new_asset, estate.Estate):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(-1)
        elif isinstance(new_asset, station.Station):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(-1)
        elif isinstance(new_asset, utility.Utility):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(-1)
        else:
            pass

    def remove_asset(self, old_asset):
        """
        docstring here
        :type old_asset: estate.Estate, station.Station, utility.Utility
        :param self: self
        """
        import station
        import utility
        import estate
        if isinstance(old_asset, estate.Estate):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
        elif isinstance(old_asset, station.Station):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
        elif isinstance(old_asset, utility.Utility):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
        else:
            pass
