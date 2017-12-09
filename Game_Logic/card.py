from abc import ABCMeta, abstractmethod
import ef
import operation


class Card(metaclass=ABCMeta):
    """
    Card Class
    """

    def __init__(self, name, description):
        self._name = name
        self._description = description

    @abstractmethod
    def play(self, gamer, data):
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

    def play(self, gamer, data):
        """
        Move player on the map to certain block
        """
        print(self.description)
        if gamer.position < self._destination:
            print("Do not pass Go, no cash collected.")
        else:
            print("Passing Go, Gain 200")
            operation.pay(data['epic_bank'], gamer, 200, data)
        if self._destination == 10:
            # in jail
            gamer.cur_status = 0
        gamer.move(steps=None, position=self._destination)


class PayCard(Card):
    def __init__(self, name, card_type, description, amount):
        super().__init__(name, description)
        self._amount = amount
        self._card_type = card_type

    def play(self, gamer, data):
        """
        :param from_role: a player or bank or rest players
        :param data: global game data
        """
        print(self.description)
        if self._card_type == 2:
            to_role = data['epic_bank']
            from_role = gamer
            operation.pay(from_role, to_role, self._amount, data)
        elif self._card_type == 8:  # need to check
            to_role = []
            all_role = data["player_dict"]
            for role_id in all_role.keys():
                if role_id != gamer.id:
                    to_role.append(all_role[role_id])
            from_role = gamer
            total_amount = self._amount * len(to_role)
            for role in to_role:
                operation.pay(from_role, role, self._amount, data)
        elif self._card_type == 3:
            import estate
            from_role = gamer
            total_amount = 0
            for e in from_role.assets:
                if isinstance(estate, estate.Estate):
                    house_repair_amount = int(
                        e.house_num % 6) * self._amount[0]
                    hotel_repair_amount = int(
                        e.house_num / 6) * self._amount[1]
                    total_amount += house_repair_amount + hotel_repair_amount
                    operation.pay(
                        from_role, data['epic_bank'], self._amount, data)

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

    def play(self, gamer, data):
        """
        :param from_role: a player or bank or rest players
        :param from_role: player or bank or rest players
        """
        print(self.description)
        if self._card_type == 0:
            to_role = gamer
            operation.pay(data['epic_bank'], to_role, self._amount, data)
        elif self._card_type == 1:
            to_role = gamer
            from_role = []
            all_role = data["player_dict"]
            for role_id in all_role.keys():
                if role_id != gamer.id:
                    from_role.append(role_id)
            for role_id in from_role:
                payer = all_role[role_id]
                operation.pay(payer, gamer, self._amount, data)

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

    def play(self, gamer, data):
        """
        Baild card, can be collected by players
        """
        to_role = gamer
        print(self.description)
        if to_role.bail_card_num == 0:
            print("1. Keep it yourself.")
            print("2. Sell to others.")
            while True:
                input_str = input("Please enter the number of your decision:")
                try:
                    choice = int(input_str)
                    if choice == 1 or choice == 2:
                        break
                    elif choice == -1:
                        return False
                    else:
                        print("Invaild choice, please input again.")
                except ValueError:
                    print("Please enter a number. Enter -1 to quit")
            if choice == 1:
                to_role.bail_card_num = to_role.bail_card_num + 1
            elif choice == 2:
                while True:
                    input_str = input(
                        "Please enter the player of you want to sell the card to:")
                    try:
                        choice = str(input_str)
                        if choice in data['player_dict'].keys() and choice != gamer.name:
                            break
                        elif choice == 'q':
                            return False
                        else:
                            print("Invaild choice, please input again.")
                    except ValueError:
                        print("Please enter a player name. Enter q to quit")
                to_role = data['player_dict'][choice]
                from_role = gamer
                # TODO: need to implement trade
                pass
