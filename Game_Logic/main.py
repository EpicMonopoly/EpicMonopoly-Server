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
from json_io import json_reader, json_writer

# global player_dic
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
    # block_list_data = json_reader('Data/block_data.json')
    # station_list_data = json_reader('Data/station_data.json')
    # utility_list_data = json_reader('Data/utility_data.json')
    # estate_list_data = json_reader('Data/estate_data.json')
    # chest_list_data = json_reader('Data/chest_data.json')
    # chance_list_data = json_reader('Data/chance_data.json')
    block_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/block_data.json')
    station_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/station_data.json')
    utility_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/utility_data.json')
    estate_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/estate_data.json')
    chest_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/chest_data.json')
    chance_list_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/chance_data.json')
    block_list = []
    station_list = []
    utility_list = []
    estate_list = []
    for b in block_list_data:
        if b['block_type'] == 0:  # ["Go", "Go to jail", "In Jail", "Free Parking"]
            block_list.append(block.Block(b['name'], b['position']))
        elif b['block_type'] == 1:  # ["Community Chest", "Chance"]
            block_list.append(cardpile.CardPile(b['name'], b['position']))
        elif b['block_type'] == 2:  # ["Income Tax", "Super Tax"]
            block_list.append(tax.Tax(b['name'], b['position'], 0.10))
        else:
            pass
        block_list.append(b)
    for s in station_list_data:  # name, position, uid, estate_value, status, street_id
        station_list.append(station.Station(s['name'], s['position'], s['uid'], s['estate_value'], s['status']))
    for u in utility_list_data:  # name, position, uid, estate_value, status, street_id
        utility_list.append(utility.Utility(u['name'], u['position'], u['uid'], u['estate_value'], u['status']))
    for e in estate_list_data:
        estate_list.append(estate.Estate(e['name'], e['position'], e['uid'], e['estate_value'], e['status'], 0, 200))

    # initialize chess board
    chess_board = board.Board([], [], [], block_list, [], [])

    # initialize players
    player_dict_data = json_reader('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/player_list.json')
    player_dict = {}
    for i in range(len(player_dict_data)):
        p = player.Player(player_dict_data[i]['id'], player_dict_data[i]['name'], player_dict_data[i]['cash'],
                          player_dict_data[i]['alliance'])
        player_dict[player_dict_data[i]['id']] = p

    # initialize bank
    epic_bank = bank.Bank('99', 'EpicBank')
    json_writer('/home/caesar/Documents/Code/EpicMonopoly-Server/Data/bank_data.json', {"house_number": epic_bank.cur_house, "hotel_number": epic_bank.cur_hotel})

    # initialize chest
    chest_list = []
    for chest in chest_list_data:
        if chest['card_type'] == 0 or chest['card_type'] == 1:  # 0: Collection, 1: Collect_from_players
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
            chest_list.append(card.BailCard(chest['card_id'], chest['card_type'], chest['description']))
    chance_list = []
    for chance in chance_list_data:
        if chance['card_type'] == 0:  # 0: Collection
                                    # or chance['card_type'] == 1, 1: Collect_from_players
            chance_list.append(card.CollectCard(chance['card_id'], chance['card_type'], chance['description'],
                                                chance['amount']))
        elif chance['card_type'] == 2 or chance['card_type'] == 3 or chance['card_type'] == 8:  # 2: Pay,
                                                                                                # 3: Pay_for_repair
                                                                                                # 8: Pay_to_players
            chance_list.append(card.PayCard(chance['card_id'], chance['card_type'], chance['description'],
                                            chance['amount']))
        elif chance['card_type'] == 4 or chance['card_type'] == 6:  # 4: Move_indicate_position, 6: Move_nearby
            chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                             chance['block_id']))
        elif chance['card_type'] == 7:  # Move
            chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                             chance['steps']))
        elif chance['card_type'] == 5:  # Bailcard
            chance_list.append(card.BailCard(chance['card_id'], chance['card_type'], chance['description']))

    # initialize chance
    global data_dict
    data_dict['chess_board'] = chess_board
    data_dict['player_dict'] = player_dict
    data_dict['epic_bank'] = epic_bank
    data_dict['chest_list'] = chest_list
    data_dict['chance_list'] = chance_list
    return data_dict

def roll(gamer):
    """
    Roll a dice
    :type gamer: player.Player
    :param gamer: The player who roll dices
    Returns:
    :int: The number of first dice
    :int: The number of second dice
    :bool: The station of end_flag
    """
    # Whether pass Go
    print("Rolling")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    if a == b:
        end_flag = False
    else:
        end_flag = True
    print("Dice number is", a, b)
    step = a + b
    current_gamer_position = gamer.position
    if current_gamer_position + step > 40:
        operation.pay(data_dict['epic_bank'], gamer, 200)
    gamer.move(step)
    end_position = gamer.position
    current_block = data_dict['chess_board'].get_block(end_position)
    current_block.display(player, data_dict)
    return a, b, end_flag

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


def construct_building(gamer):
    if data["epic_bank"].cur_house == 0:
        print("Bank out of house")
        return 0
    own_street = own_all_block(gamer)
    print("Valid building list")
    asset_number_list = []
    for cur_asset in gamer.properties:
        if isinstance(cur_asset, estate.Estate):
            if cur_asset.street_id in own_street:
                print("No.%d %s" %(cur_asset.block_id, cur_asset.name))
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
                operation.pay(gamer, data["epic_bank"], payment)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_hotel()
                print("%s built one hotel in %s" %(gamer.name, cur_asset.name))
            elif cur_asset.house_num == 4:
                if data["epic_bank"].cur_hotel == 0:
                    print("Bank out of hotel")
                    return 0
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    print("Do not have enough money")
                    return 0
                operation.pay(gamer, data["epic_bank"], payment)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_hotel()
                data["epic_bank"].remove_house(4)
                print("%s built one hotel in %s" %(gamer.name, cur_asset.name))
            else:
                payment = cur_asset.house_value
                if payment > gamer.cash:
                    print("Do not have enough money")
                    return 0
                operation.pay(gamer, data["epic_bank"], payment)
                cur_asset.house_num(cur_asset.house_num + 1)
                data["epic_bank"].built_house()
                print("%s built one house in %s" %(gamer.name, cur_asset.name))

def turn(gamer):
    """
    :type gamer: player.Player
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
        choice = int(input("Please enter the number of your decision:"))
        print(choice)
        if choice == 1:
            operation.trade()
        elif choice == 2:
            dice_a, dice_b, end_flag = roll(gamer)
        elif choice == 3:
            construct_building(gamer)
        elif choice == 4:
            operation.mortgage_asset()
        elif choice == 5:
            if end_flag is True:
                break
            else:
                print("Please roll a dice")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    data = init_game()
    living_list = data["player_dict"].keys()
    data["living_list"] = living_list
    while len(living_list) != 1:
        for gamer_id in living_list:
            gamer = data["player_dict"][gamer_id]
            turn(gamer)
