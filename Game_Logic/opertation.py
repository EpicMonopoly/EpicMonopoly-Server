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


def broken(gamer):
    pass