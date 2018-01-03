import sys
import role


class Bank(role.Role):
    """
    subclass(Role): Bank
    """

    def __init__(self, uid, name, house_number, hotel_number):
        """
        Constructor
        loan_list: set
        cur_house: int
        cur_hotel: int
        """
        super().__init__(uid, name, sys.maxsize)
        self._loan_dict = {}
        self._cur_house = house_number
        self._cur_hotel = hotel_number

    @property
    def loan_list(self):
        """
        Return load list
        """
        return self._loan_dict

    @property
    def cur_house(self):
        """
        Return current valid house number
        """
        return self._cur_house

    @property
    def cur_hotel(self):
        """
        Return current valid house number
        """
        return self._cur_hotel

    def pay(self, payment):
        # bank never pays anything
        pass

    def gain(self, payment):
        # bank seems like gaining a lot
        pass

    def built_house(self):
        self._cur_house = self.cur_house - 1

    def built_hotel(self):
        self._cur_hotel = self._cur_hotel - 1

    def remove_house(self, number):
        self._cur_house = self.cur_house + number

    def remove_hotel(self):
        self._cur_hotel = self._cur_hotel + 1

    # # TODO: test
    # def add_loan_dict(self, gamer, assets_id, amount):
    #     import player
    #     for asset_id in assets_id:
    #         for a in gamer.assets:
    #             if a.block_id == asset_id:
    #                 gamer.remove_asset(a)
    #                 self._loan_dict[asset_id] = a

    # # TODO: test
    # def remove_loan_dict(self, assets_id):
    #     for asset_id in assets_id:
    #         if asset_id in self._loan_dict.keys():
    #             del self._loan_dict[asset_id]

    # # TODO: test
    # def repayment(self, from_role, assets):
    #     """
    #     Repay the mortgaged assets
    #     :type from_role: player.Player
    #     :type assets: list
    #     :param from_role: player
    #     :param assets: a set of assets
    #     :return: True or not of this repayment
    #     """
    #     import station
    #     import utility
    #     import estate
    #     repay_value = 0
    #     if assets:
    #         for a in assets:
    #             if isinstance(a, station.Station):
    #                 repay_value += a.mortgage_value
    #                 self._loan_dict[from_role.name] = a
    #             elif isinstance(a, utility.Utility):
    #                 repay_value += a.mortgage_value
    #                 self._loan_dict[from_role.name] = a
    #             elif isinstance(a, estate.Estate):
    #                 repay_value += a.mortgage_value
    #                 self._loan_dict[from_role.name] = a
    #         from_role.gain(repay_value)
    #         return True
    #     else:
    #         return False

    def add_asset(self, new_asset):
        """
        Add asset to bank
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
        Remove an asset from bank
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

    def getJSON(self):
        """
        Return data according to bank.json
        """
        json_data = {
            "type": "bank",
            "data": [
                {
                    "house_num": self._cur_house,
                    "hotel_num": self._cur_hotel
                }
            ]
        }
        return json_data
