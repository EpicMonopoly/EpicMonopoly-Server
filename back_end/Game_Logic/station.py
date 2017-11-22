import asset


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
                print("%s own %s" % (gamer.name, self.name))
            else:
                # Other pass this station
                print("%s own %s" % (owner.name, self.name))
                fee = self.payment(gamer.station_num)
                operation.pay(gamer, owner, fee, data)
        elif self._status == -1:
            # Nobody own
            while True:
                print("Nobody own %s do you want to buy it?" % self.name)
                print("1: Buy it")
                print("2: Do not buy it")
                while True:
                    input_str = input("Please enter the number of your decision:")
                    try:
                        choice = int(input_str)
                        break
                    except ValueError:
                        print("Please enter a number.")
                print()
                if choice == 1:
                    price = self.value
                    if price > gamer.cash:
                        print("You do not have enough money")
                        break
                    else:
                        operation.pay(gamer, bank, price, data)
                        operation.trade_asset(self, bank, gamer)
                        print("%s buy %s for %d" %
                              (gamer.name, self.name, price))
                        break
                elif choice == 2:
                    break
                else:
                    print("Invalid operation")
        elif self._status == 0:
            # In mortgage
            print("%s is in mortgaged" % self.name)
        else:
            raise ValueError("Invalid estate status")
