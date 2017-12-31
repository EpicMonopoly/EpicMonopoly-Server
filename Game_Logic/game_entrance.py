# The main control of the game

import os
import random
from collections import OrderedDict

import bank
import block
import board
import card
import cardpile
import color
import ef
import estate
import messager
import operation
import player
import station
import tax
import utility
from json_io import json_reader, json_writer

data = None


def init_game(mess_hand):
    """
    Initialize the game with map, players and bank
    """
    global data
    data['msg'] = mess_hand
    chess_board = board.Board(mess_hand)
    data = chess_board.get_data()
    return data


def roll(gamer, data):
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
    step = a + b
    current_gamer_position = gamer.position
    if current_gamer_position + step > 40:
        go_block = data["chess_board"][0]
        operation.pay(data['epic_bank'], gamer, go_block.reward, data)
        operation.push2all("Passing Go, Gain %d" % go_block.reward)
    gamer.move(step)
    end_position = gamer.position
    current_block = data['chess_board'][end_position]
    if isinstance(current_block, block.Go_To_Jail):
        end_flag = True
    operation.push2all("At %s" % current_block.name)
    current_block.display(gamer, data, step)
    return a, b, end_flag


def roll_dice():
    operation.push2all("Rolling")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    operation.push2all("Dice number is %d %d" % (a, b))
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


def add_player(p):
    global data
    data["living_list"].append(p.id)
    data["player_dict"][p.id] = p


def turn(gamer, data):
    """
    :param gamer: players
    :return:
    """
    end_flag = False
    while True:
        operation.push2all("1: Trade with others")
        operation.push2all("2: Roll dices")
        operation.push2all("3: Construct building")
        operation.push2all("4: Remove building")
        operation.push2all("5: Mortgage asset")
        operation.push2all("6: End turn")
        while True:
            input_str = operation.wait_choice(
                "Please enter the number of your decision:")
            if(True):
                input_data = data["msg"].get_json_data("input")
                input_str = input_data[0]["request"]
                print("input_str", input_str)
            try:
                choice = int(input_str)
                break
            except ValueError:
                operation.push2all("Please enter a number.")
        operation.push2all()
        if choice == 1:
            # operation.trade(data, trade_data)
            pass
        elif choice == 2 and end_flag is False:
            dice_a, dice_b, end_flag = roll(gamer, data)
        elif choice == 3:
            operation.construct_building(gamer, data)
        elif choice == 4:
            operation.remove_building(gamer, data)
        elif choice == 5:
            operation.mortgage_asset(gamer, data)
        elif choice == 6:
            if end_flag is True:
                break
            else:
                operation.push2all("Please roll a dice")
        else:
            operation.push2all("Invalid choice")


def start_game(mess_hand):
    global data
    data = init_game(mess_hand)
    living_list = list(data["player_dict"].keys())
    data["living_list"] = living_list
    num_round = 0
    update_period = 1
    while len(living_list) != 1:
        if num_round % update_period == 0:
            operation.update_value(data)
        num_round += 1
        for gamer_id in living_list:
            gamer = data["player_dict"][gamer_id]
            operation.push2all("Now is %s turn" % gamer.name)
            operation.push2all("Gamer current cash %d" % gamer.cash)
            if gamer.cur_status == 0:
                # In jail
                operation.push2all("%s are in jail" % gamer.name)
                a, b = roll_dice()
                if a == b:
                    gamer.cur_status = 1
                    gamer._in_jail = 0
                    turn(gamer, data)
                else:
                    while True:
                        operation.push2all("1: Bail. Get out of prison.")
                        operation.push2all("2: Stay in prison.")
                        while True:
                            input_str = operation.wait_choice(
                                "Please enter the number of your decision:")
                            if(True):
                                input_data = data["msg"].get_json_data("input")
                                input_str = input_data[0]["request"]
                            try:
                                choice = int(input_str)
                                break
                            except ValueError:
                                operation.push2all("Please enter a number.")
                        operation.push2all()
                        if choice == 1:
                            if operation.bail(gamer, data):
                                gamer.cur_status = 1
                                gamer._in_jail = 0
                                turn(gamer, data)
                                break
                            else:
                                operation.push2all("Please stay in jail")
                                gamer.count_in_jail()
                                break
                        elif choice == 2:
                            gamer.count_in_jail()
                            break
                        else:
                            operation.push2all("Invalid choice")
            elif gamer.cur_status == 1:
                # Normal Status
                turn(gamer, data)
            else:
                pass
            operation.push2all()


if __name__ == "__main__":
    # start_game()
    pass
