from abc import ABCMeta, abstractmethod
from property import Property


class Role(metaclass=ABCMeta):
    """
    Abstract class: Role
    """

    def __init__(self, uid, name, cash):
        """
        Constructor of Role
        uid: int
        name: string
        cash: int
        property: set of Property
        """
        self._uid = uid
        self._name = name
        self._cash = cash
        self._properties = set()  # Property[]

    @property  # getUid
    def owner(self):
        return self._uid

    @property  # getName
    def name(self):
        return self._name

    @property  # getCash
    def cash(self):
        return self._cash

    # @cash.setter
    # def cash(self, value):
    #     self._cash += value

    @property  # getProperties
    def properties(self):
        return self._properties

    def add_property(self, properties):
        """
        Add property to properties
        :type properties: Property
        :param properties: Property
        """
        self._properties.add(properties)

    def remove_property(self, properties):
        """
        Remove property from properties
        :type properties: set of Property
        :param properties: properties set
        :return boolean: True if succeed while False if properties is empty
        """
        if self._properties:
            for p in properties:
                self._properties.remove(p)
            return True
        else:
            return False

    @abstractmethod
    def trade_property(self, properties, from_role, to_role):
        """
        Trade for other players or bank
        :param properties: Property
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade successfully or not
        """
        pass

    @abstractmethod
    def pay(self, amount, from_role, to_role):
        """
        Trade cash between players or bank
        :param amount: amount of cash to be traded
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade finished or error
        """
        pass
