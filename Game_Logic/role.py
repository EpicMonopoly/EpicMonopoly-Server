from abc import ABCMeta, abstractmethod


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
        self._assets = set()  # Property[]

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
        return self._assets

    @abstractmethod
    def add_asset(self, new_asset):
        """
        Add property to properties
        :type new_asset: asset.Asset
        :param new_asset: assets
        """
        pass

    @abstractmethod
    def remove_asset(self, assets):
        """
        Remove asset from assets
        :type assets: list
        :param assets: assets
        :return boolean: True if succeed while False if asset is empty
        """
        pass
