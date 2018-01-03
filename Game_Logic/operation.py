import json
import uuid
import game_entrance
import push_service

msg_queue = []


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
        data["msg"].push2all(gen_record_json(
            "%s pay %d to %s" % (payer.name, payment, gainer.name)))
        data["msg"].push2all(gen_record_json("%s out of cash" % payer.name))
        clearing(payer, payment_left, data)
    else:
        payer.pay(payment)
        gainer.gain(payment)
        data["msg"].push2all(gen_record_json(
            "%s pay %d to %s" % (payer.name, payment, gainer.name)))


def bail(prionser, data):
    jail = data["chess_board"][prionser.position]
    bail_fee = jail.bail_fee(prionser.in_jail_time)
    if prionser.cash < bail_fee:
        data["msg"].push2single(prionser.id, gen_hint_json("No enough money"))
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
    to_role.add_asset(new_asset)g
    new_asset.clear_log()


def clearing(gamer, amount_left, data):
    """
    docstring here
    :param gamer:
    :param amount_left:
    """
    record = "Start mortgage " + str(gamer.name) + "'s assets"
    data["msg"].push2all(gen_hint_json(record))
    data["msg"].push2all(gen_record_json(record))
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


def trade(data, trade_data):
    import asset
    # Get infomation
    gamer_a_dict = trade_data["data"][0]
    gamer_b_dict = trade_data["data"][1]
    gamer_a = data["player_dict"][gamer_a_dict["player_id"]]
    gamer_b = data["player_dict"][gamer_b_dict["player_id"]]
    # Check validation
    valid_flag = True
    if gamer_a.cash < gamer_a_dict["money_give"]:
        valid_flag = False
    if gamer_b.cash < gamer_b_dict["money_give"]:
        valid_flag = False
    for asset_index in gamer_a_dict["asset_give"]:
        asset_trade = data["chess_board"][asset_index]
        if isinstance(asset_trade, asset.Asset) is False:
            valid_flag = False
        else:
            if asset_index not in gamer_a.assets and asset_trade.status != 1:
                valid_flag = False
    for asset_index in gamer_b_dict["asset_give"]:
        asset_trade = data["chess_board"][asset_index]
        if isinstance(asset_trade, asset.Asset) is False:
            valid_flag = False
        else:
            if asset_index not in gamer_b.assets:
                valid_flag = False
    if gamer_a.bail_card_num < gamer_a_dict["card_give"]:
        valid_flag = False
    if gamer_b.bail_card_num < gamer_b_dict["card_give"]:
        valid_flag = False
    if valid_flag is False:
        return False
    # Comfirm trade
    if gamer_a_dict["money_give"] != 0:
        pay(gamer_a, gamer_b, gamer_a_dict["money_give"], data)
    if gamer_b_dict["money_give"] != 0:
        pay(gamer_b, gamer_a, gamer_b_dict["money_give"], data)
    for asset_index in gamer_a_dict["asset_give"]:
        asset_trade = data["chess_board"][asset_index]
        trade_asset(asset_trade, gamer_a, gamer_b)
    for asset_index in gamer_b_dict["asset_give"]:
        asset_trade = data["chess_board"][asset_index]
        trade_asset(asset_trade, gamer_b, gamer_a)
    if gamer_a_dict["card_give"] != 0:
        gamer_a.bail_card_num += -1
        gamer_b.bail_card_num += 1
    if gamer_b_dict["card_give"] != 0:
        gamer_b.bail_card_num += -1
        gamer_a.bail_card_num += 1
    return True


def update_value(data):
    block_list = data["chess_board"]
    chest_list = data["chest_list"]
    chance_list = data["chance_list"]
    ef = data["ef"]
    ef.generate_ef()
    for b in block_list:
        b.change_value(ef.random_rate())
    for c in chest_list:
        c.change_value(ef.ef_value)
    for c in chance_list:
        c.change_value(ef.ef_value)


def broken(gamer, data):
    data["player_dict"][gamer.id].cur_status = -1
    data["living_list"].remove(gamer.id)
    for cur_asset in gamer.assets:
        trade_asset(cur_asset, gamer, data["epic_bank"])
        data["epic_bank"].remove_loan_dict(cur_asset.block_id)
    record = str(gamer.name) + "bankrupt"
    data["msg"].push2all(gen_record_json("%s bankrupt" % gamer.name))


def mortgage_asset(gamer, data):
    # data["msg"].push2single(gamer.id, gen_hint_json("Your current assets"))
    asset_number_list = []
    for cur_asset in gamer.assets:
        if cur_asset.status == 1:
            # data["msg"].push2single(gamer.id, gen_hint_json(
            #     "No.%d %s" % (cur_asset.block_id, cur_asset.name)))
            asset_number_list.append(cur_asset.block_id)
    if asset_number_list == []:
        # data["msg"].push2single(gamer.id, gen_hint_json("None"))
        return 0
    input_str = data["msg"].get_json_data("input")
    while not input_str:
        input_str = data["msg"].get_json_data("input")
    input_str = input_str[0]["request"]
    asset_number = int(input_str)
    data["msg"].push2all()
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            data["msg"].push2single(gamer.id, gen_hint_json("Invalid input"))
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
    # data["msg"].push2single(gamer.id, gen_hint_json("Valid building list"))
    print("Valid building list")
    asset_number_list = []
    for cur_asset in gamer.assets:
        if isinstance(cur_asset, estate.Estate):
            if cur_asset.street_id in own_street and (cur_asset.status == 1 or cur_asset.status == 2):
                # data["msg"].push2single(gamer.id, gen_hint_json(
                #     "No.%d %s" % (cur_asset.block_id, cur_asset.name)))
                print("No.%d %s" % (cur_asset.block_id, cur_asset.name))
                asset_number_list.append(cur_asset.block_id)
    if asset_number_list == []:
        # data["msg"].push2single(gamer.id, gen_hint_json("None"))
        print("None")
        return 0
    input_str = data["msg"].get_json_data("input")
    while not input_str:
        input_str = data["msg"].get_json_data("input")
    input_str = input_str[0]["request"]
    asset_number = int(input_str)
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            data["msg"].push2single(gamer.id, gen_hint_json("Invalid input"))
            return 0
    for cur_asset in gamer.assets:
        if cur_asset.block_id == asset_number:
            if cur_asset.house_num == 6:
                data["msg"].push2single(
                    gamer.id, gen_hint_json("Cannot built more house!"))
                return 0
            elif cur_asset.house_num == 5:
                if data["epic_bank"].cur_hotel == 0:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Bank out of hotel"))
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Do not have enough money"))
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                data["epic_bank"].built_hotel()
                record = str(gamer.name) + " built one hotel in " + \
                    str(cur_asset.name)
                data["msg"].push2all(gen_record_json(gen_hint_json(
                    "%s built one hotel in %s" % (gamer.name, cur_asset.name))))
            elif cur_asset.house_num == 4:
                if data["epic_bank"].cur_hotel == 0:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Bank out of hotel"))
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Do not have enough money"))
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                cur_asset.status = 2
                data["epic_bank"].built_hotel()
                data["epic_bank"].remove_house(4)
                data["msg"].push2all(gen_record_json(
                    "%s built one hotel in %s" % (gamer.name, cur_asset.name)))
            else:
                if data["epic_bank"].cur_house == 0:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Bank out of house"))
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    data["msg"].push2single(
                        gamer.id, gen_hint_json("Do not have enough money"))
                    return 0
                pay(gamer, data["epic_bank"], payment, data)
                cur_asset.house_num = cur_asset.house_num + 1
                cur_asset.status = 2
                data["epic_bank"].built_house()
                data["msg"].push2all(gen_record_json(
                    "%s built one house in %s" % (gamer.name, cur_asset.name)))


def remove_building(gamer, data):
    import estate
    # data["msg"].push2single(
    #     gamer.id, gen_hint_json("Valid remove building list"))
    print("Valid remove building list")
    asset_number_list = []
    for cur_asset in gamer.assets:
        if cur_asset.state == 2:
            print("No.%d %s" % (cur_asset.block_id, cur_asset.name))
            asset_number_list.append(cur_asset.block_id)
    if asset_number_list == []:
        # data["msg"].push2single(gamer.id, gen_hint_json("None"))
        print("None")
        return 0
    input_str = data["msg"].get_json_data("input")
    while not input_str:
        input_str = data["msg"].get_json_data("input")
    input_str = input_str[0]["request"]
    asset_number = int(input_str)
    if asset_number == -1:
        return 0
    else:
        if asset_number not in asset_number_list:
            data["msg"].push2single(gamer.id, gen_hint_json("Invalid input"))
            return 0
    for cur_asset in gamer.assets:
        if cur_asset.block_id == asset_number:
            if cur_asset.house_num > 0:
                epic_bank = data["epic_bank"]
                cur_asset.house_num += -1
                pay(epic_bank, gamer, cur_asset.house_value / 2, data)
                epic_bank.remove_house(1)
                if cur_asset.house_num == 0:
                    cur_asset.status == 1


def gen_hint_json(msg):
    """
    generate hint message in json format
    """
    return_json = {}
    return_json["type"] = "hint"
    return_json["data"] = [{"message": msg}]
    return json.dumps(return_json)


def gen_record_json(msg):
    """
    generate record message in json format
    """
    return_json = {}
    return_json["type"] = "record"
    return_json["data"] = [{"message": msg}]
    return json.dumps(return_json)


def gen_dice_result_dict(a, b, gamer):
    """
    generate the result of dice in json format
    """
    result_dict = {}
    result_dict["type"] = "dice_result"
    result_dict["data"] = [{"dice_result": [a, b], "player_id": gamer.id}]
    return result_dict


def gen_newturn_json(gamer):
    """
    generate new turn data in json format
    """
    result_dict = {}
    result_dict["type"] = "newturn"
    result_dict["data"] = [{"id": gamer.id}]
    return json.dumps(result_dict)


def gen_choice_json(msg):
    """
    generate choice input in json format
    """
    return_json = {}
    return_json["type"] = "choice"
    return_json["data"] = [{"message": msg}]
    return json.dumps(return_json)


def gen_init_json(data):
    """
    generate initialization data in json format
    """
    data_list = []
    json_block = {
        "type": "block"
    }
    block_list_a = []
    for i in data["chess_board"]:
        block_list_a.append(i.getJSON_block())
    json_block["data"] = block_list_a
    json_estate = {
        "type": "estate"
    }
    block_list_b = []
    for i in data["estate_list"]:
        block_list_b.append(i.getJSON())
    json_estate["data"] = block_list_b
    json_station = {
        "type": "station"
    }
    block_list_c = []
    for i in data["station_list"]:
        block_list_c.append(i.getJSON())
    json_station["data"] = block_list_c
    json_utility = {
        "type": "utility"
    }
    block_list_d = []
    for i in data["utility_list"]:
        block_list_d.append(i.getJSON())
    json_utility["data"] = block_list_d
    json_player = {
        "type": "player"
    }
    block_list_e = []
    for i in data["player_dict"]:
        block_list_e.append(data["player_dict"][i].getJSON())
    json_player["data"] = block_list_e
    json_ef = {
        "type": "ef",
        "data": [data["ef"].getJSON()]
    }
    init_dict = {
        "type": "init",
        "data": [json_block, json_estate, json_station, json_utility, json_player, json_ef]
    }
    return json.dumps(init_dict)


def gen_update_json(data):
    """
    generate update data in json format
    """
    data_list = []
    json_estate = {
        "type": "estate"
    }
    block_list_b = []
    for i in data["estate_list"]:
        block_list_b.append(i.getJSON())
    json_estate["data"] = block_list_b
    json_station = {
        "type": "station"
    }
    block_list_c = []
    for i in data["station_list"]:
        block_list_c.append(i.getJSON())
    json_station["data"] = block_list_c
    json_utility = {
        "type": "utility"
    }
    block_list_d = []
    for i in data["utility_list"]:
        block_list_d.append(i.getJSON())
    json_utility["data"] = block_list_d
    json_player = {
        "type": "player"
    }
    block_list_e = []
    for i in data["player_dict"]:
        block_list_e.append(data["player_dict"][i].getJSON())
    json_player["data"] = block_list_e
    json_ef = {
        "type": "ef",
        "data": [data["ef"].getJSON()]
    }
    init_dict = {
        "type": "update",
        "data": [json_estate, json_station, json_utility, json_player, json_ef]
    }
    print(init_dict)
    return json.dumps(init_dict)


# def push2all(line=""):
#     mess = game_entrance.get_mess_hand()
#     return mess.push2all(line)


# def wait_choice():
#     """
#     Wait for front end to upload data
#     """
#     mess = game_entrance.get_mess_hand()
#     return mess.wait_choice()


# def push2single(uid, line=""):
#     mess = game_entrance.get_mess_hand()
#     return mess.push2single(uid, line)

# def some_method(data):
#     line = "" # 要推送的的信息
#     uid = "" # 推送对象
#     # 单个推送
#     data["msg"].push2single(uid, line)
#     # 广播
#     data["msg"].push2all(line)
#     # 等待消息
#     data["msg"].wait_choice()
