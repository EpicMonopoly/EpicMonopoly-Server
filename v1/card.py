# encoding: utf-8
from abc import ABCMeta, abstractmethod


class Card(metaclass=ABCMeta):
    def __init__(self, name, description):
        self._name = name
        self._description = description

    @abstractmethod
    def play(self):
        pass

    @property
    def name(self):  # getter
        return self._name

    @property
    def description(self):  # getter
        return self._description

    @abstractmethod
    def change_value(self, EF):
        pass


class MoveCard(Card):
    def __init__(self, name, description, step):
        super().__init__(name, description)
        self._destination = step

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, step):
        """
        :param step: int position in map
        """
        self._destination = step

    def play(self):
        # how to go to destination
        pass


class PunishCard(Card):
    def __init__(self, name, description, amount):
        super().__init__(name, description)
        self._amount = amount

    def play(self, from_role, to_role):
        # how to go to punish
        pass

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def change_value(self, EF):
        pass


class RewardCard(Card):
    def __init__(self, name, description, amount):
        super().__init__(name, description)
        self._amount = amount

    def play(self, from_role, to_role):
        # how to go to punish
        pass

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def change_value(self, EF):
        pass
