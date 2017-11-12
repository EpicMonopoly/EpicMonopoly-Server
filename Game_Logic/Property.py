from abc import abstractclassmethod
from block import Block


class Property(Block):
    """
    Class Property
    """

    def __init__(self):
        """
        Call constructor of superclass
        name(super): string
        position(super): int
        uid: int
        estate_value: int
        status: int
        street_id: int
        """
        super().__init__()
        self._uid = int()
        self._estate_value = int()
        self._status = int()
        self._street_id = int()

    @property  # setOwner
    def owner(self):
        return self._uid

    @owner.setter  # getOwner
    def owner(self, uid):
        self._uid = uid

    @property  # getValue
    def value(self):
        return self._estate_value

    # @property
    # def value(self, estate_value):
    #     self._estate_value = estate_value

    @property  # getStatus
    def status(self):
        return self._status

    @status.setter  # setStatus
    def status(self, status):
        self._status = status

    mortgage_rate = 0.5

    @property  # getMortgageValue
    def mortgage_value(self):
        return self._estate_value * self.mortgage_rate

    # TODO: add changeEF method
    # def changeEF(self):
    #     pass

    @property  # getPayment
    def payment(self):
        return self._estate_value

    @property  # getPosition
    def street_id(self):
        return self._street_id

    @street_id.setter  # setPosition
    def street_id(self, street_id):
        self._street_id = street_id

    @abstractclassmethod
    def display(self):
        pass
