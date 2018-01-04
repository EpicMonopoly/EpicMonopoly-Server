import asset
import operation


class Utility(asset.Asset):
    """Class Utility

    Parameters
    ----------
    asset.Asset: 

    """

    def __init__(self, name, block_id, position, uid, estate_value, status):
        """constructor

        Parameters
        ----------
        self: class itself
        name: name of utility
        block_id: block id of utility
        position: position of utility
        uid: owner id of utility
        estate_value: estate value of utility
        status: status of utility

        """
        super().__init__(name, block_id, position, uid, estate_value, status)

    def payment(self, utility_num, dice_result):
        """payment

        Parameters
        ----------
        self: class itself
        utility_num: number of utility
        dice_result: result of dice

        Returns
        -------
        payment: amount of payment
        """
        if utility_num == 1:
            return dice_result * 4
        elif utility_num == 2:
            return dice_result * 10
        else:
            # Should not be here
            return 0

    def change_value(self, rate):
        """change estate value

        Parameters
        ----------
        self: class itself
        rate: rate of change

        """
        self._estate_value = int(self._estate_value * (1 + rate))

    def display(self, gamer, data, dice_result):
        """display message when entering the utility

        Parameters
        ----------
        self: class itself
        gamer: gamer object
        data: data dict
        dice_result: result of dice

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
                passing_time = 0
                if gamer.id in self.enter_log:
                    passing_time = self.enter_log[gamer.id]
                    self.enter_log[gamer.id] += 1
                else:
                    self.enter_log[gamer.id] = 1
                data["msg"].push2all(operation.gen_record_json(
                    "%s own %s" % (gamer.name, self.name)))
                payment = self.payment(
                    gamer.utility_num, dice_result) * (0.9 ** passing_time)
                if gamer.alliance == owner.alliance:
                    # Make discount to alliance
                    payment = payment * 0.9
                    data['msg'].push2single(gamer.id, operation.gen_hint_json(
                        "%s and %s are alliances, make discount" % (owner.name, gamer.name)))
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

    def getJSON(self):
        """get data in JSON format

        Parameters
        ----------
        self: class itself

        Returns
        -------
        json_data: data in json format
        """
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
