import asset
import operation


class Station(asset.Asset):
    """
    Class Station
    """

    def __init__(self, name, block_id, position, uid, estate_value, status):
        """
        Call for superclass construct
        """
        super().__init__(name, block_id, position, uid, estate_value, status)

    def payment(self, station_num):
        """
        Return the payment if a player enter this block
        :param station_num: number of station
        :return: amount of payment

        """
        return self._get_payment(station_num)

    def _get_payment(self, station_num):
        value = self._estate_value
        if station_num == 1:
            return (1 / 8) * value
        elif station_num == 2:
            return (1 / 4) * value
        elif station_num == 3:
            return (1 / 2) * value
        elif station_num == 4:
            return value
        else:
            # Should not be here
            return 0

    def change_value(self, rate):
        self._estate_value = self._estate_value * (1 + rate)

    @property
    def block_id(self):
        return self._block_id

    def display(self, gamer, data, dice_result):
        """
        Display description
        :type data: dict
        :return:
        """
        import operation
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
                fee = self.payment(gamer.station_num) * (0.9 ** passing_time)
                if gamer.alliance == owner.alliance:
                    # Make discount to alliance
                    fee = fee * 0.9
                    data['msg'].push2single(gamer.id, operation.gen_hint_json(
                        "%s and %s are alliances, make discount" % (owner.name, gamer.name)))
                operation.pay(gamer, owner, fee, data)
        elif self._status == -1:
            # Nobody own
            while True:
                # data["msg"].push2single(gamer.id, operation.gen_hint_json(
                #     "Nobody own %s do you want to buy it?" % self.name))
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
        payment_list = []
        for i in range(1, 5):
            payment_list.append(
                {"station_number": i, "payment": self._get_payment(i)})
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
            "uid": self._uid,
            "estate_value": self._estate_value,
            "status": self._status,
            "mortgage_value": self.mortgage_value,
            "payment": payment_list
        }
        return json_data
