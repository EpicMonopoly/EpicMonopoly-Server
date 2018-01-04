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

    @abstractmethod
    def change_value(self, rate):
        pass

    def getJSON(self):
        json_data = {
            "description": self._description
        }
        return json_data


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
        # data['msg'].push2single(
        #     gamer.id, operation.gen_hint_json(self.description))
        data['msg'].push2all(operation.gen_hint_json(
            "player %s get card: %s" % (gamer.name, self.description)))
        if isinstance(self._destination, list):
            tmp = self._destination[0]
            for dest in self._destination:
                if gamer.position < dest:
                    tmp = dest
                    data['msg'].push2single(gamer.id, operation.gen_hint_json(
                        "Do not pass Go, no cash collected."))
                    gamer.move(steps=None, position=tmp)
                    break
                else:
                    continue
            go_block = data["chess_board"][0]
            data['msg'].push2single(gamer.id, operation.gen_hint_json(
                "Passing Go, Gain %d" % go_block.reward))
            operation.pay(data['epic_bank'], gamer, go_block.reward, data)
            gamer.move(steps=None, position=tmp)
            dest_block = data["chess_board"][tmp]
            dest_block.display(gamer, data, 0)
        else:
            if gamer.position < self._destination:
                data['msg'].push2single(gamer.id, operation.gen_hint_json(
                    "Do not pass Go, no cash collected."))
            else:
                go_block = data["chess_board"][0]
                data['msg'].push2single(gamer.id, operation.gen_hint_json(
                    "Passing Go, Gain %d" % go_block.reward))
                operation.pay(data['epic_bank'], gamer, go_block.reward, data)
            if self._destination == 10:
                # in jail
                gamer.cur_status = 0
            gamer.move(steps=None, position=self._destination)
            dest_block = data["chess_board"][self._destination]
            dest_block.display(gamer, data, 0)

    def change_value(self, rate):
        pass

    # def getJSON(self):
    #     json_data = {
    #         "name": self._name,
    #         "description": self._description,
    #         "destination": self._destination,
    #         "card_type": self._card_type
    #     }
    #     return json_data


class PayCard(Card):
    def __init__(self, name, card_type, description, amount):
        super().__init__(name, description)
        self._amount = amount
        self._card_type = card_type

    def change_value(self, rate):
        """
        Change the value of payment card
        """
        self._amount = int(self._amount * (1 + rate))

    def play(self, gamer, data):
        """
        :param from_role: a player or bank or rest players
        :param data: global game data
        """
        data['msg'].push2all(operation.gen_hint_json(
            "player %s get card: %s" % (gamer.name, self.description)))
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

    # def getJSON(self):
    #     json_data = {
    #         "name": self._name,
    #         "description": self._description,
    #         "amount": self._amount,
    #         "card_type": self._card_type
    #     }
    #     return json_data


class CollectCard(Card):
    def __init__(self, name, card_type, description, amount):
        super().__init__(name, description)
        self._amount = amount
        self._card_type = card_type

    def change_value(self, rate):
        pass

    def play(self, gamer, data):
        """
        :param from_role: a player or bank or rest players
        :param from_role: player or bank or rest players
        """
        # data['msg'].push2single(
        #     gamer.id, operation.gen_hint_json(self.description))
        data['msg'].push2all(operation.gen_hint_json(
            "player %s get card: %s" % (gamer.name, self.description)))
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

    # def getJSON(self):
    #     json_data = {
    #         "name": self._name,
    #         "description": self._description,
    #         "amount": self._amount,
    #         "card_type": self._card_type
    #     }
    #     return json_data


# class BailCard(Card):
#     def __init__(self, name, card_type, description):
#         super().__init__(name, description)
#         self._card_type = card_type

#     def change_value(self, rate):
#         pass

#     def play(self, gamer, data):
#         """
#         Baild card, can be collected by players
#         """
#         to_role = gamer
#         # data['msg'].push2single(
#         #     gamer.id, operation.gen_hint_json(self.description))
#         data['msg'].push2all(operation.gen_hint_json("player %s get card: %s" % (gamer.name, self.description)))
#         if to_role.bail_card_num == 0:
#             data['msg'].push2single(
#                 gamer.id, operation.gen_hint_json("1. Keep it yourself."))
#             data['msg'].push2single(
#                 gamer.id. operation.gen_hint_json("2. Sell to others."))
#             input_str = data['msg'].get_json_data("input")
#             while not input_str:
#                 input_str = data['msg'].get_json_data("input")
#             choice = int(input_str)
#             if choice == 1:
#                 to_role.bail_card_num = to_role.bail_card_num + 1
#             elif choice == 2:
#                 data['msg'].push2single(
#                     gamer.id, operation.gen_hint_json("Players list:"))
#                 for p in data['player_dict']:
#                     data['msg'].push2single(
#                         gamer.id, operation.gen_hint_json(p['name']))
#                 input_str = data['msg'].gen_json_data("input")
#                 while not input_str:
#                     input_str = data["msg"].get_json_data("input")
#                 choice = str(input_str)
#                 if choice not in data['player_dict'].keys() or choice == gamer.name:
#                     data['msg'].push2single(gamer.id, operation.gen_hint_json(
#                         "Invaild choice, please input again."))
#                 else:
#                     to_role = data['player_dict'][choice]
#                     from_role = gamer
#                     # TODO: need to implement trade
#                     pass
#             else:
#                 data['msg'].push2single(
#                     gamer.id, operation.gen_hint_json("Invaild choice."))

    # def getJSON(self):
    #     json_data = {
    #         "name": self._name,
    #         "description": self._description,
    #         "card_type": self._card_type
    #     }
    #     return json_data
