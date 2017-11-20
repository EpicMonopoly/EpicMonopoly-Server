import estate
import utility
import station
import bank
import role
import player

def pay(payer, gainer, payment):
    """
    docstring here
        :param payer: Payer
        :param gainer: Gainer
        :param payment: Amount
    """
    cash_A = payer.cash
    if cash_A < payment:
        # payer broken
        pass
    else:
        payer.pay(payment)
        gainer.gain(payment)
        print("%s pay %d to %s" % (payer.name, payment, gainer.name))

def trade_property(self, new_property, from_role, to_role):
    """
    Trade for other players or bank
    :type to_role: role.Role
    :type from_role: role.Role
    :param new_property: Property
    :param from_role: from_role
    :param to_role: to_role
    :return boolean: Trade successfully or not
    """
    from_role.remove_property(new_property)
    to_role.add_property(new_property)
        