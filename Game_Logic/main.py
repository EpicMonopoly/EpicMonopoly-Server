# The main control of the game

import random
import board
import player
import bank
import block
import cardpile
import tax
import estate
import station
import utility
import card
import operation
from json_io import json_reader, json_writer
import os

# global data_dict
data_dict = {}


def init_game():
    """
    Initialize the game with map, players and bank
    1. generate a map
    2. initialize players
    3. initialize bank
    all of the data
    :return: map, players list and bank
    """
    # generate a map
    parent_addr = os.path.abspath(os.pardir)
    block_list_data = json_reader(os.path.join(
        parent_addr, 'Data/block_data.json'))
    station_list_data = json_reader(os.path.join(
        parent_addr, 'Data/station_data.json'))
    utility_list_data = json_reader(os.path.join(
        parent_addr, 'Data/utility_data.json'))
    estate_list_data = json_reader(os.path.join(
        parent_addr, 'Data/estate_data.json'))
    chest_list_data = json_reader(os.path.join(
        parent_addr, 'Data/chest_data.json'))
    chance_list_data = json_reader(os.path.join(
        parent_addr, 'Data/chance_data.json'))
    block_list = [0 for x in range(40)]
    station_list = []
    utility_list = []
    estate_list = []
    corner_list = []
    chest_block_list = []
    chance_block_list = []
    tax_list = []

    # initialize bank
    epic_bank = bank.Bank('99', 'EpicBank')
    json_writer(os.path.join(parent_addr, 'Data/bank_data.json'),
                {"house_number": epic_bank.cur_house, "hotel_number": epic_bank.cur_hotel})

    for b in block_list_data["data"]:
        if b['block_type'] == 0:
            # ["Go", "Go to Jail", "In Jail", "Free Parking"]
            if b['name'] == "Go":
                corner_block = block.Go(
                    b['name'], b['block_id'], b['position'])
            elif b['name'] == "Go to Jail":
                corner_block = block.Go_To_Jail(
                    b['name'], b['block_id'], b['position'])
            elif b['name'] == "In Jail":
                corner_block = block.In_Jail(
                    b['name'], b['block_id'], b['position'])
            elif b['name'] == "Free Parking":
                corner_block = block.Free_Parking(
                    b['name'], b['block_id'], b['position'])
            else:
                pass
            block_list[corner_block.position] = corner_block
            corner_list.append(corner_block)
        elif b['name'] == "Community Chest":
            # "Community Chest"
            new_block = cardpile.Community_Chest(
                b['name'], b['block_id'], b['position'])
            block_list[new_block.position] = new_block
            chest_block_list.append(new_block)
        elif b['name'] == "Chance":  # "Chance"
            new_block = cardpile.Chance(
                b['name'], b['block_id'], b['position'])
            block_list[new_block.position] = new_block
            chance_block_list.append(new_block)
        elif b['block_type'] == 3:
            # ["Income Tax", "Super Tax"]
            if b['name'] == "Income Tax":
                new_block = tax.Income_Tax(
                    b['name'], b['block_id'], b['position'], 0.10)
            elif b['name'] == "Super Tax":
                new_block = tax.Super_Tax(
                    b['name'], b['block_id'], b['position'], 0.10)
            else:
                pass
            block_list[new_block.position] = new_block
            tax_list.append(new_block)
    # name, position, uid, estate_value, status, street_id
    for s in station_list_data["data"]:
        new_block = station.Station(
            s['name'], s['block_id'], s['position'], s['uid'], s['estate_value'], s['status'])
        station_list.append(new_block)
        block_list[new_block.position] = new_block
        epic_bank.add_asset(new_block)
    # name, position, uid, estate_value, status, street_id
    for u in utility_list_data["data"]:
        new_block = utility.Utility(
            u['name'], u['block_id'], u['position'], u['uid'], u['estate_value'], u['status'])
        utility_list.append(new_block)
        block_list[new_block.position] = new_block
        epic_bank.add_asset(new_block)
    for e in estate_list_data["data"]:
        new_block = estate.Estate(e['name'], e['block_id'], e['position'], e['uid'],
                                  e['estate_value'], e['status'], e['street_id'], e['house_value'])
        estate_list.append(new_block)
        block_list[new_block.position] = new_block
        epic_bank.add_asset(new_block)

    # initialize players
    player_dict_data = json_reader(os.path.join(
        parent_addr, 'Data/player_list.json'))
    player_dict = {}
    player_dict_data = player_dict_data["data"]
    for i in range(len(player_dict_data)):
        p = player.Player(player_dict_data[i]['id'], player_dict_data[i]['name'], player_dict_data[i]['cash'],
                          player_dict_data[i]['alliance'])
        print(p.cash, p.id, p.name, p.alliance)
        player_dict[player_dict_data[i]['id']] = p

    # initialize chest cards
    chest_list = []
    for chest in chest_list_data["data"]:
        # 0: Collection, 1: Collect_from_players
        if chest['card_type'] == 0 or chest['card_type'] == 1:
            chest_list.append(card.CollectCard(chest['card_id'], chest['card_type'], chest['description'],
                                               chest['amount']))
        elif chest['card_type'] == 2 or chest['card_type'] == 3:  # 2: Pay, 3: Pay_for_repair
                                                                # or chest['card_type'] == 8 8: Pay_to_players
            chest_list.append(card.PayCard(chest['card_id'], chest['card_type'], chest['description'],
                                           chest['amount']))
        # elif chest['card_type'] == 4 or chest['card_type'] == 6:  # 4: Move_indicate_position, 6: Move_nearby
        #     chest_list.append(card.MoveCard(chest['card_id'], chest['card_type'], chest['description'],
        #                                     chest['block_id']))
        # elif chest['card_type'] == 7:  # Move
        #     chest_list.append(card.MoveCard(chest['card_id'], chest['card_type'], chest['description'],
        #                                     chest['steps']))
        elif chest['card_type'] == 5:  # Bailcard
            chest_list.append(card.BailCard(
                chest['card_id'], chest['card_type'], chest['description']))

    # initialize chance cards
    chance_list = []
    for chance in chance_list_data["data"]:
        if chance['card_type'] == 0:  # 0: Collection
                                    # or chance['card_type'] == 1, 1: Collect_from_players
            chance_list.append(card.CollectCard(chance['card_id'], chance['card_type'], chance['description'],
                                                chance['amount']))
        elif chance['card_type'] == 2 or chance['card_type'] == 3 or chance['card_type'] == 8:  # 2: Pay,
                                                                                                # 3: Pay_for_repair
                                                                                                # 8: Pay_to_players
            chance_list.append(card.PayCard(chance['card_id'], chance['card_type'], chance['description'],
                                            chance['amount']))
        # 4: Move_indicate_position, 6: Move_nearby
        elif chance['card_type'] == 4 or chance['card_type'] == 6:
            chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                             chance['block_id']))
        elif chance['card_type'] == 7:  # Move
            chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                             chance['steps']))
        elif chance['card_type'] == 5:  # Bailcard
            chance_list.append(card.BailCard(
                chance['card_id'], chance['card_type'], chance['description']))

    # initialize chess board
    two_block_street = []
    three_block_street = []
    for e in estate_list:
        if e.street_id == 1 or e.street_id == 8:
            two_block_street.append(e)
        else:
            three_block_street.append(e)
    chess_board_object = board.Board(two_block_street, three_block_street, station_list, utility_list, block_list,
                                     corner_list, chest_block_list, chance_block_list, tax_list)

    global data_dict
    data_dict['chess_board'] = block_list
    data_dict['player_dict'] = player_dict
    data_dict['epic_bank'] = epic_bank
    data_dict['chest_list'] = chest_list
    data_dict['chance_list'] = chance_list
    data_dict['station_list'] = station_list
    data_dict['utility_list'] = utility_list
    data_dict['estate_list'] = estate_list
    data_dict['corner_list'] = corner_list
    data_dict['chest_block_list'] = chest_block_list
    data_dict['chance_block_list'] = chance_block_list
    data_dict['tax_list'] = tax_list
    return data_dict


def roll(gamer):
    """
    Roll a dice
    :param gamer: The player who roll dices
    Returns:
    :int: The number of first dice
    :int: The number of second dice
    :bool: The station of end_flag
    """
    # Whether pass Go
    a, b = roll_dice()
    if a == b:
        end_flag = False
    else:
        end_flag = True
    print("Dice number is", a, b)
    step = a + b
    current_gamer_position = gamer.position
    if current_gamer_position + step > 40:
        print("Passing Go, Gain 200")
        operation.pay(data_dict['epic_bank'], gamer, 200, data_dict)
    gamer.move(step)
    end_position = gamer.position
    current_block = data_dict['chess_board'][end_position]
    if isinstance(current_block, block.Go_To_Jail):
        end_flag = True
    print("At %s" % current_block.name)
    current_block.display(gamer, data_dict, step)
    return a, b, end_flag


def roll_dice():
    print("Rolling")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    return a, b


def own_all_block(gamer):
    block_number = [0 for x in range(9)]
    own_street = []
    for cur_asset in gamer.properties:
        if isinstance(cur_asset, estate.Estate):
            block_number[cur_asset.street_id] = block_number[cur_asset.street_id] + 1
    for i in range(9):
        if block_number[i] == 3:
            own_street.append(i)
    if block_number[1] == 2:
        own_street.append(1)
    if block_number[8] == 2:
        own_street.append(8)
    return own_street


def turn(gamer):
    """
    :param gamer: players
    :return:
    """
    end_flag = False
    while True:
        print("1: Trade with others")
        print("2: Roll dices")
        print("3: Construct building")
        print("4: Mortgage asset")
        print("5: End turn")
        while True:
            input_str = input("Please enter the number of your decision:")
            try:
                choice = int(input_str)
                break
            except ValueError:
                print("Please enter a number.")
        print()
        if choice == 1:
            operation.trade()
        elif choice == 2 and end_flag is False:
            dice_a, dice_b, end_flag = roll(gamer)
        elif choice == 3:
            operation.construct_building(gamer, data)
        elif choice == 4:
            operation.mortgage_asset(gamer, data)
        elif choice == 5:
            if end_flag is True:
                break
            else:
                print("Please roll a dice")
        else:
            print("Invalid choice")


if __name__ == "__main__":
    data = init_game()
    living_list = list(data["player_dict"].keys())
    data["living_list"] = living_list
    while len(living_list) != 1:
        for gamer_id in living_list:
            gamer = data["player_dict"][gamer_id]
            print("Now is %s turn" % gamer.name)
            print("Gamer current cash %d" % gamer.cash)
            if gamer.cur_status == 0:
                # In jail
                print("%s are in jail" % gamer.name)
                a, b = roll_dice()
                if a == b:
                    gamer.cur_status = 1
                    gamer._in_jail = 0
                    turn(gamer)
                else:
                    while True:
                        print("1: Bail. Get out of prison.")
                        print("2: Stay in prison.")
                        while True:
                            input_str = input(
                                "Please enter the number of your decision:")
                            try:
                                choice = int(input_str)
                                break
                            except ValueError:
                                print("Please enter a number.")
                        print()
                        if choice == 1:
                            if operation.bail(gamer, data):
                                gamer.cur_status = 1
                                gamer._in_jail = 0
                                turn(gamer)
                                break
                            else:
                                print("Please stay in jail")
                                gamer.count_in_jail()
                                break
                        elif choice == 2:
                            gamer.count_in_jail()
                            break
                        else:
                            print("Invalid choice")
            elif gamer.cur_status == 1:
                # Normal Status
                turn(gamer)
            else:
                pass
            print()
