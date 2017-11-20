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
from json_io import json_reader, json_writer

# global player_dic
global data_dic


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
    block_list_data = json_reader('Data/block_data.json')
    station_list_data = json_reader('Data/station_data.json')
    utility_list_data = json_reader('Data/utility_data.json')
    estate_list_data = json_reader('Data/estate_data.json')
    chest_list_data = json_reader('Data/chest_data.json')
    chance_list_data = json_reader('Data/chance_data.json')
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
            block_list.append(tax.Tax(b['name'], b['position'], 0.17))
        else:
            pass
        block_list.append(b)
    for s in station_list_data:  # name, position, uid, estate_value, status, street_id
        station_list.append(station.Station(s['name'], s['position'], s['uid'], s['estate_value'], s['status']))
    for u in utility_list_data:  # name, position, uid, estate_value, status, street_id
        utility_list.append(utility.Utility(u['name'], u['position'], u['uid'], u['estate_value'], u['status']))
    for e in estate_list_data:
        estate_list.append(estate.Estate(e['name'], e['position'], e['uid'], e['estate_value'], e['status'], 0, 200))

    chess_board = board.Board([], [], [], block_list, [], [])

    # initialize players
    player_list_data = json_reader('Data/player_list.json')
    # player_list = []  # type player.Player
    player_dic = {}
    for i in range(len(player_list_data)):
        p = player.Player(player_list_data[i]['id'], player_list_data[i]['name'], player_list_data[i]['cash'],
                          player_list_data[i]['alliance'])
        player_dic[player_list_data[i]['id']] = p
    data_dic["player_dic"] = player_dic

    # initialize bank
    epic_bank = bank.Bank('99', 'EpicBank')
    json_writer('Data/bank_data.json', {"house_number": epic_bank.cur_house, "hotel_number": epic_bank.cur_hotel})
    return chess_board, player_list, epic_bank



def trade():
    pass


def roll(player):
    """
    Roll a dice
    :type player: player.Player
    :param player: The player who roll dices
    Returns:
    :int: The number of first dice
    :int: The number of second dice
    :bool: The station of end_flag
    """
    print("Rolling")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    if a == b:
        end_flag = False
    else:
        end_flag = True
    print("Dice number is", a, b)
    step = a + b
    player.move(step)
    end_position = player.position
    current_block = chess_board.get_block(end_position)
    current_block.display(player, data_dic)
    return a, b, end_flag

def construct_building():
    pass


def mortgage_property():
    pass


def turn(player):
    """
    :type player: player.Player
    :param player:
    :return:
    """
    end_flag = False
    while True:
        print("1: Trade with others")
        print("2: Roll dices")
        print("3: Construct building")
        print("4: Mortgage property")
        print("5: End turn")
        choice = int(input("Please enter the number of your decision:"))
        print(choice)
        if choice == 1:
            trade()
        elif choice == 2:
            dice_a, dice_b, end_flag = roll(player)
        elif choice == 3:
            construct_building()
        elif choice == 4:
            mortgage_property()
        elif choice == 5:
            if end_flag is True:
                break
            else:
                print("Please roll a dice")
        else:
            print("Invalid choice")

def broken(player, amount_need):
    pass

if __name__ == "__main__":
    chess_board, players, epic_bank = init_game()
