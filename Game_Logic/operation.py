# operations

def pay(payer, gainer, payment):
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
    :type to_role: role.Role
    :type from_role: role.Role
    :param new_asset: asset.Asset
    :param from_role: from_role
    :param to_role: to_role
    :return boolean: Trade successfully or not
    """
    from_role.remove_asset(new_asset)
    to_role.add_asset(new_asset)


def clearing(gamer, amount_left):
    """
    docstring here
        :param gamer:
        :param amount_left:
    """
    pass


def trade():
    pass

def broken(gamer):
    pass

def mortgage_asset(gamer, data):
    print("Your current assets")
    asset_number_list = []
    for cur_asset in gamer.properties:
        print("No.%d %s"%(cur_asset.block_id, cur_asset.name))
        asset_number_list.append(cur_asset.block_id)
    asset_number = int(input("Please enter the number you want to mortgage"))
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            print("Invalid input")
            return 0
    for cur_asset in gamer.properties:
        if cur_asset.block_id == asset_number:
            return_cash = cur_asset.mortgage_value
            pay(data["epic_bank"], gamer, return_cash)
            cur_asset.status(0)
            data["epic_bank"].add_loan_dict(cur_asset.block_id, return_cash)
