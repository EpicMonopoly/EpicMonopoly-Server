# operations
def pay(payer, gainer, payment, data):
    """
    Paying
        :param payer: Payer
        :param gainer: Gainer
        :param payment: Amount
    """
    cash_A = payer.cash
    if cash_A < payment:
        payment_left = payment - cash_A
        pass
    else:
        payer.pay(payment)
        gainer.gain(payment)
        print("%s pay %d to %s" % (payer.name, payment, gainer.name))


def trade_asset(new_asset, from_role, to_role):
    """
    Trade for other players or bank
    :param new_asset: asset.Asset
    :param from_role: from_role
    :param to_role: to_role
    :return boolean: Trade successfully or not
    """
    from_role.remove_asset(new_asset)
    to_role.add_asset(new_asset)


# TODO: implement this method
def clearing(gamer, amount_left, data):
    """
    docstring here
    :param gamer:
    :param amount_left:
    """
    # for cur_asset in gamer.assets:
    #     pass


# TODO: implement trade methods
def trade():
    pass


def broken(gamer, data):
    data["living_list"].remove(gamer.id)
    data["player_dict"][gamer.id].cur_status = -1
    for cur_asset in gamer.properties:
        trade_asset(cur_asset, gamer, data["epic_bank"])
        data["epic_bank"].remove_loan_dict(cur_asset.block_id)
    print("%s bankrupt" % gamer.name)


def mortgage_asset(gamer, data):
    print("Your current assets")
    asset_number_list = []
    for cur_asset in gamer.properties:
        print("No.%d %s" % (cur_asset.block_id, cur_asset.name))
        asset_number_list.append(cur_asset.block_id)
    while True:
        input_str = input("Please enter the index you want to mortgage:")
        try:
            asset_number = int(input_str)
            break
        except ValueError:
            print("Please enter a number. Enter -1 to quit")
    print()
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            print("Invalid input")
            return 0
    for cur_asset in gamer.properties:
        if cur_asset.block_id == asset_number:
            return_cash = cur_asset.mortgage_value
            pay(data["epic_bank"], gamer, return_cash, data)
            cur_asset.status = 0
            data["epic_bank"].add_loan_dict(cur_asset.block_id, return_cash)


def own_all_block(gamer):
    return []


def construct_building(gamer, data):
    import estate
    if data["epic_bank"].cur_house == 0:
        print("Bank out of house")
        return 0
    own_street = own_all_block(gamer)
    print("Valid building list")
    asset_number_list = []
    for cur_asset in gamer.properties:
        if isinstance(cur_asset, estate.Estate):
            if cur_asset.street_id in own_street:
                print("No.%d %s" % (cur_asset.block_id, cur_asset.name))
                asset_number_list.append(cur_asset.block_id)
    if asset_number_list is []:
        print("None")
        return 0
    while True:
        input_str = input("Please enter the number you want to built a house")
        try:
            asset_number = int(input_str)
            break
        except ValueError:
            print("Please enter a number. Enter -1 to quit")
    print()
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            print("Invalid input")
            return 0
    for cur_asset in gamer.properties:
        if cur_asset.block_id == asset_number:
            if cur_asset.house_num == 6:
                print("Cannot built more house!")
                return 0
            elif cur_asset.house_num == 5:
                if data["epic_bank"].cur_hotel == 0:
                    print("Bank out of hotel")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    print("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_hotel()
                print("%s built one hotel in %s" %
                      (gamer.name, cur_asset.name))
            elif cur_asset.house_num == 4:
                if data["epic_bank"].cur_hotel == 0:
                    print("Bank out of hotel")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    print("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_hotel()
                data["epic_bank"].remove_house(4)
                print("%s built one hotel in %s" %
                      (gamer.name, cur_asset.name))
            else:
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    print("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_house()
                print("%s built one house in %s" %
                      (gamer.name, cur_asset.name))
