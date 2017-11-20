import role
import bank
import estate
import station
import utility
import property


class Player(role.Role):
    """
    subclass(Role): Player
    """

    def __init__(self, uid, name, cash, alliance):
        """
        Constructor
        :param uid: int
        :param name: string
        :param cash: int
        :param alliance: string
        """
        super().__init__(uid, name, cash)
        self._alliance = alliance
        self._position = 0
        self._bail_card_num = 0
        self._cur_status = 1
        self._utility_num = 0
        self._station_num = 0

    @property  # getAlliance
    def alliance(self):
        return self._alliance

    @property
    def position(self):
        return self._position

    # @position.setter
    # def position(self, position):
    #     self._position = position

    @property
    def bail_card_num(self):
        return self._bail_card_num

    @bail_card_num.setter  # changeBailCard
    def bail_card_num(self, bail_card_num):
        self._bail_card_num = bail_card_num

    @property  # get currentStatus
    def cur_status(self):
        return self._cur_status

    @cur_status.setter  # changeStatus
    def cur_status(self, cur_status):
        self._cur_status = cur_status

    @property
    def utility_num(self):
        return self._utility_num

    # @utility_num.setter
    # def utility_num(self, utility_num):
    #     self._utility_num = utility_num

    @property
    def station_num(self):
        return self._station_num

    # @station_num.setter
    # def station_num(self, station_num):
    #     self._station_num = station_num

    def pay(self, amount):
        self._cash = self._cash - amount
    
    def gain(self, amount):
        self._cash = self._cash + amount

    def calculat_asset_value(self):
        total_asset_value = self.cash
        for p in self.properties:
            total_asset_value = total_asset_value + p.value
        return total_asset_value
    
    def add_property(self, new_property):
        """
        Add property to player
        :type new_property: property.Property
        """
        if isinstance(new_property, estate.Estate):
            self._properties.add(new_property)
            new_property.owner(self.id)
            new_property.status(1)
        elif isinstance(new_property, station.Station):
            self._properties.add(new_property)
            new_property.owner(self.id)
            new_property.status(1)
            self._station_num = self._station_num + 1
        elif isinstance(new_property, utility.Utility):
            self._properties.add(new_property)
            new_property.owner(self.id)
            new_property.status(1)
            self._utility_num = self._utility_num + 1
        else:
            pass
    
    def remove_property(self, old_property):
        """
        docstring here
            :param self: 
            :type old_property: property.Property
        """
        if isinstance(new_property, estate.Estate):
            self._properties.remove(old_property)
            new_property.owner(self.id)
            new_property.status(-1)
        elif isinstance(new_property, station.Station):
            self._properties.remove(old_property)
            new_property.owner(self.id)
            new_property.status(-1)
            self._station_num = self._station_num - 1
        elif isinstance(new_property, utility.Utility):
            self._properties.remove(old_property)
            new_property.owner(self.id)
            new_property.status(-1)
            self._utility_num = self._utility_num - 1
        else:
            pass

    def move(self, steps, position=None):
        """
        Move players
        :type steps: int
        :type position: int
        :param steps: steps to move
        :param position: position to arrive(actually go into jail or something else)
        position: None if normally move on map otherwise set the position
        """
        if not position:
            self._position += steps
        else:
            self._position = position

