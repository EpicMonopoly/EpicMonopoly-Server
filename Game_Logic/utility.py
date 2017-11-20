import asset


class Utility(asset.Asset):
    """
    Class Utility
    """
    def __init__(self, name, position, uid, estate_value, status):
        """
        Call superclass construct method
        """
        super().__init__(name, position, uid, estate_value, status)

    def payment(self, utility_num, dice_result):
        if utility_num == 1:
            return dice_result * 4
        elif utility_num == 2:
            return dice_result * 10
        else:
            # Should not be here
            return 0

    # TODO: implement display
    def display(self, gamer, data_dict, dice_result):
        """
        Display description
        :type data_dict: dict
        :type gamer: player.Player
        :return:
        """
        import operation
        player_dict = data_dict['player_dict']
        bank = data_dict['bank']
        if self._status == 1:
            # Some body own it
            owner_id = self.owner()
            owner = player_dict[owner_id]
            if owner_id == gamer.id:
                # Owner pass this station
                print("%s own %s" % (gamer.name, self.name))
            else:
                # Other pass this station
                payment = self.payment(gamer.utility_num, dice_result)
                operation.pay(gamer, owner, payment)
        elif self._status == -1:
            # Nobody own
            while True:
                print("Nobody own %s do you want to buy it?" % self.name)
                print("1: Buy it")
                print("2: Do not buy it")
                choice = int(
                    input("Please enter the number of your decision:"))
                if choice == 1:
                    price = self.value
                    if price > gamer.cash:
                        print("You do not have enough money")
                        break
                    else:
                        operation.pay(gamer, bank, price)
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
