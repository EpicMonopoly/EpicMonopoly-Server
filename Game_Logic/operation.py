import uuid
import chatdemo


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
        payer.pay(cash_A)
        gainer.gain(payment)
        push2all("%s pay %d to %s" % (payer.name, payment, gainer.name))
        push2all("%s out of cash" % payer.name)
        clearing(payer, payment_left, data)
    else:
        payer.pay(payment)
        gainer.gain(payment)
        push2all("%s pay %d to %s" % (payer.name, payment, gainer.name))


def bail(prionser, data):
    jail = data["chess_board"][prionser.position]
    bail_fee = jail.bail_fee
    if prionser.cash < bail_fee:
        push2all("Not enough money")
        return False
    else:
        pay(prionser, data["epic_bank"], bail_fee, data)
        return True


def trade_asset(new_asset, from_role, to_role):
    """
    Trade for other players or bank
    :param new_asset: new_asset
    :param from_role: from_role
    :param to_role: to_role
    :return boolean: Trade successfully or not
    """
    from_role.remove_asset(new_asset)
    to_role.add_asset(new_asset)


def clearing(gamer, amount_left, data):
    """
    docstring here
    :param gamer:
    :param amount_left:
    """
    push2all("Start mortgage %s's assets" % gamer.name)
    for cur_asset in gamer.assets:
        if amount_left <= 0:
            return 0
        return_cash = mortgage(gamer, cur_asset, data)
        if amount_left - return_cash < 0:
            pay(gamer, data["epic_bank"], amount_left, data)
            amount_left = 0
        else:
            pay(gamer, data["epic_bank"], return_cash, data)
            amount_left = amount_left - return_cash
    broken(gamer, data)


def trade():
    pass


def update_value(data):
    block_list = data["chess_board"]
    ef = data["ef"]
    ef.generate_ef()
    for b in block_list:
        b.change_value(ef.random_rate())


def broken(gamer, data):
    data["player_dict"][gamer.id].cur_status = -1
    data["living_list"].remove(gamer.id)
    for cur_asset in gamer.assets:
        trade_asset(cur_asset, gamer, data["epic_bank"])
        data["epic_bank"].remove_loan_dict(cur_asset.block_id)
    push2all("%s bankrupt" % gamer.name)


def mortgage_asset(gamer, data):
    push2all("Your current assets")
    asset_number_list = []
    for cur_asset in gamer.assets:
        if cur_asset.status == 1:
            push2all("No.%d %s" % (cur_asset.block_id, cur_asset.name))
            asset_number_list.append(cur_asset.block_id)
    if asset_number_list == []:
        push2all("None")
        return 0
    while True:
        input_str = wait_choice("Please enter the index you want to mortgage:")
        try:
            asset_number = int(input_str)
            break
        except ValueError:
            push2all("Please enter a number. Enter -1 to quit")
    push2all()
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            push2all("Invalid input")
            return 0
    for cur_asset in gamer.assets:
        if cur_asset.block_id == asset_number:
            return_cash = cur_asset.mortgage_value
            pay(data["epic_bank"], gamer, return_cash, data)
            cur_asset.status = 0
            data["epic_bank"].add_loan_dict(cur_asset.block_id, return_cash)


def mortgage(gamer, mortgage_property, data):
    return_cash = mortgage_property.mortgage_value
    pay(data["epic_bank"], gamer, return_cash, data)
    mortgage_property.status = 0
    data["epic_bank"].add_loan_dict(mortgage_property.block_id, return_cash)
    return return_cash


def own_all_block(gamer):
    """
    Check which street the gamer own
    """
    import estate
    all_block = [0 for x in range(9)]
    own_street = []
    for cur_asset in gamer.assets:
        if isinstance(cur_asset, estate.Estate):
            all_block[cur_asset.street_id] += 1
    for i in range(9):
        if all_block[i] == 3:
            own_street.append(i)
    if all_block[1] == 2:
        own_street.append(1)
    if all_block[8] == 2:
        own_street.append(8)
    return own_street


def construct_building(gamer, data):
    import estate
    own_street = own_all_block(gamer)
    push2all("Valid building list")
    asset_number_list = []
    for cur_asset in gamer.assets:
        if isinstance(cur_asset, estate.Estate):
            if cur_asset.street_id in own_street:
                push2all("No.%d %s" % (cur_asset.block_id, cur_asset.name))
                asset_number_list.append(cur_asset.block_id)
    if asset_number_list == []:
        push2all("None")
        return 0
    while True:
        input_str = wait_choice(
            "Please enter the number you want to built a house:")
        try:
            asset_number = int(input_str)
            break
        except ValueError:
            push2all("Please enter a number. Enter -1 to quit")
    push2all()
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            push2all("Invalid input")
            return 0
    for cur_asset in gamer.assets:
        if cur_asset.block_id == asset_number:
            if cur_asset.house_num == 6:
                push2all("Cannot built more house!")
                return 0
            elif cur_asset.house_num == 5:
                if data["epic_bank"].cur_hotel == 0:
                    push2all("Bank out of hotel")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    push2all("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                data["epic_bank"].built_hotel()
                push2all("%s built one hotel in %s" %
                         (gamer.name, cur_asset.name))
            elif cur_asset.house_num == 4:
                if data["epic_bank"].cur_hotel == 0:
                    push2all("Bank out of hotel")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    push2all("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                data["epic_bank"].built_hotel()
                data["epic_bank"].remove_house(4)
                push2all("%s built one hotel in %s" %
                         (gamer.name, cur_asset.name))
            else:
                if data["epic_bank"].cur_house == 0:
                    push2all("Bank out of house")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    push2all("Do not have enough money")
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                data["epic_bank"].built_house()
                push2all("%s built one house in %s" %
                         (gamer.name, cur_asset.name))


def wait_choice(line=""):
    """
    Wait for front end to upload data
    """
    push2all(line)
    # Substitution for input method
    return input()
    choice = chatdemo.global_Choice.get_choice()
    while choice == -1:
        choice = chatdemo.global_Choice.get_choice()
    return choice


def push2all(line=""):
    print(line)
    message = {
        "id": str(uuid.uuid4()),
        "body": line,
    }
    # message["html"] = tornado.escape.to_basestring(.render_string("message.html", message=message))
    chatdemo.global_message_buffer.new_messages([message])
