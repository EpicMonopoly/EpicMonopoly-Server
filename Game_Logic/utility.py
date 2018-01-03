import asset
import operation


class Utility(asset.Asset):
    """
    Class Utility
    """

    def __init__(self, name, block_id, position, uid, estate_value, status):
        """
        Call superclass construct method
        """
        super().__init__(name, block_id, position, uid, estate_value, status)

    def payment(self, utility_num, dice_result):
        if utility_num == 1:
            return dice_result * 4
        elif utility_num == 2:
            return dice_result * 10
        else:
            # Should not be here
            return 0

    def change_value(self, rate):
        self._estate_value = self._estate_value * (1 + rate)

    def display(self, gamer, data, dice_result):
        """
        Display description
        :type data: dict
        :type gamer: player.Player
        :return:
        """
        # import operation
        player_dict = data['player_dict']
        bank = data['epic_bank']
        if self._status == 1:
            # Some body own it
            owner_id = self.owner
            owner = player_dict[owner_id]
            if owner_id == gamer.id:
                # Owner pass this station
                data["msg"].push2all(operation.gen_record_json(
                    "%s own %s" % (gamer.name, self.name)))
            else:
                # Other pass this station
                data["msg"].push2all(operation.gen_record_json(
                    "%s own %s" % (gamer.name, self.name)))
                payment = self.payment(gamer.utility_num, dice_result)
                if gamer.alliance == owner.alliance:
                    # Make discount to alliance
                    payment = payment * 0.9
                    data['msg'].push2single(gamer.id, operation.gen_hint_json("%s and %s are alliances, make discount" % (owner.name, gamer.name)))
                operation.pay(gamer, owner, payment, data)
        elif self._status == -1:
            # Nobody own
            while True:
                data["msg"].push2single(gamer.id, operation.gen_choice_json(
                    "Nobody own %s do you want to buy it?" % self.name))
                input_data = data["msg"].get_json_data("input")
                while input_data is False:
                    input_data = data["msg"].get_json_data("input")
                input_str = input_data[0]["request"]
                choice = int(input_str)
                if choice == 1:
                    price = self.value
                    if price > gamer.cash:
                        data["msg"].push2single(gamer.id, operation.gen_hint_json(
                            "You do not have enough money"))
                        break
                    else:
                        operation.pay(gamer, bank, price, data)
                        operation.trade_asset(self, bank, gamer)
                        data["msg"].push2all(operation.gen_record_json(
                            "%s buy %s for %d" % (gamer.name, self.name, price)))
                        break
                elif choice == 2:
                    break
                else:
                    data["msg"].push2single(
                        gamer.id, operation.gen_hint_json("Invalid operation"))
        elif self._status == 0:
            # In mortgage
            data["msg"].push2single(gamer.id, operation.gen_hint_json(
                "%s is in mortgaged" % self.name))
        else:
            raise ValueError("Invalid estate status")

    def getJSon(self):
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
            "uid": self._uid,
            "estate_value": self._estate_value,
            "status": self._status,
            "mortgage_value": self.mortgage_value,
            "payment": [{"utility_number": 1, "rate": 2}, {"utility_number": 2, "rate": 4}]
        }
        return json_data
