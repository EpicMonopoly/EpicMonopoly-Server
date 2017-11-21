from abc import ABCMeta, abstractmethod
import ef


class Card(metaclass=ABCMeta):
    """
    Card class
    """
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

    # @abstractmethod
    # def change_value(self, EF):
    #     pass


class MoveCard(Card):
    def __init__(self, name, card_type, description, step):
        super().__init__(name, description)
        self._destination = step
        self._card_type = card_type

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, step):
        """
        :param step: int position in map
        """
        self._destination = step

    def play(self, gamer):
        """
        Move player on the map to certain block
        """
        gamer.position = self._destination


class PayCard(Card):
    def __init__(self, name, card_type, description, amount):
        super().__init__(name, description)
        self._amount = amount
        self._card_type = card_type

    def play(self, from_role, to_role=None):
        """
        :param from_role: a player or bank or rest players
        :param from_role: player or bank or rest players
        """
        if self._card_type == 2:
            if from_role.cash < self._amount:
                return False
            else:
                from_role.cash = -self._amount
                to_role.cash = self._amount
                return True
        elif self._card_type == 8:  # need to check
            total_amount = len(to_role) * self._amount
            if from_role.cash < total_amount:
                return False
            else:
                from_role = -self._amount
                for role in to_role:
                    role.cash = self._amount
                return True
        elif self._card_type == 3:
            import estate
            total_amount = 0
            for e in from_role.assets:
                if isinstance(estate, estate.Estate):
                    house_repair_amount = int(e.house_num % 6) * self._amount[0]
                    hotel_repair_amount = int(e.house_num / 6) * self._amount[1]
                    total_amount += house_repair_amount + hotel_repair_amount
                    if from_role.cash < total_amount:
                        return False
                    else:
                        from_role.cash = -total_amount
                        return True
                
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def change_value(self, EF):
        pass


class CollectCard(Card):
    def __init__(self, name, card_type, description, amount):
        super().__init__(name, description)
        self._amount = amount
        self._card_type = card_type

    def play(self, from_role, to_role):
        """
        :param from_role: a player or bank or rest players
        :param from_role: player or bank or rest players
        """
        if self._card_type == 0:
            to_role.cash = self._amount
            return True
        elif self._card_type == 1:
            total_amount = 0
            broken_role = []
            for role in from_role:
                if role.cash < self._amount:
                    broken_role.append(role)
                else:
                    total_amount += self._amount
                    role.cash = -self._amount
            to_role.cash = total_amount
            return True, broken_role
        
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def change_value(self, EF):
        pass


class BailCard(Card):
    def __init__(self, name, card_type, description):
        super().__init__(name, description)
        self._card_type = card_type

    def play(self, from_role, to_role):
        """
        Baild card, can be collected by players
        """
        if from_role.bail_card_num == 0:
            print("1. Keep it yourself.")
            print("2. Sell to others.")
            choice = int(input("Please enter the number of your decision:"))
            if choice == 1:
                from_role.bail_card_num = from_role.bail_card_num + 1
            elif choice == 2:
                # TODO: need to implement the trade
                pass 


