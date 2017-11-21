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

    @property
    def cash(self):
        return 9223372036854775807  # so much money
    
    @cash.setter
    def cash(self):  # bank money will never run out
        pass

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
                    self._loan_dict[from_role.name] = a
                elif isinstance(a, utility.Utility):
                    repay_value += a.mortgage_value
                    self._loan_dict[from_role.name] = a
                elif isinstance(a, estate.Estate):
                    repay_value += a.mortgage_value
                    self._loan_dict[from_role.name] = a
            from_role.gain(repay_value)
            return True
        else:
            return False

    def add_asset(self, new_asset):
        """
        Add asset to player
        :param self: self
        """
        import station
        import utility
        import estate
        if isinstance(new_asset, estate.Estate):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = -1
        elif isinstance(new_asset, station.Station):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = -1
        elif isinstance(new_asset, utility.Utility):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = -1
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
            old_asset.owner = -1
        elif isinstance(old_asset, station.Station):
            self._assets.remove(old_asset)
            old_asset.owner = -1
        elif isinstance(old_asset, utility.Utility):
            self._assets.remove(old_asset)
            old_asset.owner = -1
        else:
            pass
