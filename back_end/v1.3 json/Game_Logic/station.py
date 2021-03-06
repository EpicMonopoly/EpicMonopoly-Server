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
                operation.push2all("%s own %s" % (gamer.name, self.name))
            else:
                # Other pass this station
                operation.push2all("%s own %s" % (owner.name, self.name))
                fee = self.payment(gamer.station_num)
                operation.pay(gamer, owner, fee, data)
        elif self._status == -1:
            # Nobody own
            while True:
                operation.push2all(
                    "Nobody own %s do you want to buy it?" % self.name)
                operation.push2all("1: Buy it")
                operation.push2all("2: Do not buy it")
                while True:
                    input_str = operation.wait_choice(
                        "Please enter the number of your decision:")
                    if(True):
                        input_data = data["msg"].get_json_data("input")
                        input_str = input_data[0]["request"]
                    try:
                        choice = int(input_str)
                        break
                    except ValueError:
                        operation.push2all("Please enter a number.")
                operation.push2all()
                if choice == 1:
                    price = self.value
                    if price > gamer.cash:
                        operation.push2all("You do not have enough money")
                        break
                    else:
                        operation.pay(gamer, bank, price, data)
                        operation.trade_asset(self, bank, gamer)
                        operation.push2all("%s buy %s for %d" %
                                           (gamer.name, self.name, price))
                        break
                elif choice == 2:
                    break
                else:
                    operation.push2all("Invalid operation")
        elif self._status == 0:
            # In mortgage
            operation.push2all("%s is in mortgaged" % self.name)
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
