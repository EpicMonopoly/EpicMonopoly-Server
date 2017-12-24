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

    def display(self, gamer, data, dice_result):
        """
        Display description
        :type data: dict
        :type gamer: player.Player
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
                payment = self.payment(gamer.utility_num, dice_result)
                operation.pay(gamer, owner, payment, data)
        elif self._status == -1:
            # Nobody own
            while True:
                operation.push2all("Nobody own %s do you want to buy it?" % self.name)
                operation.push2all("1: Buy it")
                operation.push2all("2: Do not buy it")
                while True:
                    input_str = operation.wait_choice("Please enter the number of your decision:")
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
