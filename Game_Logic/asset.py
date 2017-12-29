import block


class Asset(block.Block):
    """
    Class Asset
    """

    def __init__(self, name, block_id, position, uid, estate_value, status, mortgage_rate=0.5):
        """
        Call constructor of superclass
        name(super): string
        position(super): int
        uid: int
        estate_value: int
        status: int
        street_id: int
        """
        super().__init__(name, block_id, position)
        self._uid = uid
        self._estate_value = estate_value
        self._status = status
        self.mortgage_rate = mortgage_rate

    @property  # setOwner
    def owner(self):
        return self._uid

    @owner.setter  # getOwner
    def owner(self, uid):
        self._uid = uid

    def change_owner(self, uid):
        self._uid = uid

    @property  # getValue
    def value(self):
        return self._estate_value

    @property  # getStatus
    def status(self):
        return self._status

    @status.setter  # setStatus
    def status(self, status):
        self._status = status

    @property  # getMortgageValue
    def mortgage_value(self):
        return self._estate_value * self.mortgage_rate

    def change_value(self, rate):
        """
        Change ef value
        """
        pass

    def payment(self):
        return self._estate_value

    def display(self, gamer, data_dict, dice_result):
        pass

    def getJSon(self):
        pass
        # json_data = {
        #     "name": self._name,
        #     "block_id": self._block_id,
        #     "position": self._position,
        #     "uid": self._uid,
        #     "estate_value": self._estate_value,
        #     "status": self._status
        # }
        # return json_data
