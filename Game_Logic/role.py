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
    def id(self):
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
    
    @abstractmethod
    def add_property(self, new_property):
        """
        Add property to properties
        :type new_property: Property
        :param new_property: Property
        """
        pass

    @abstractmethod
    def remove_property(self, properties):
        """
        Remove property from properties
        :type properties: set
        :param properties: properties set
        :return boolean: True if succeed while False if properties is empty
        """
        pass