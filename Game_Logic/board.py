import random
import copy
from functools import reduce
import os
from collections import OrderedDict
import bank
import block
import card
import cardpile
import ef
import estate
# import operation
import player
import station
import tax
import utility
from json_io import json_reader, json_writer
import color


class Board:
    """
    Board class
    """

    def __init__(self, mess_hand, create_room_dict):
        """
        Initialize the board
        """
        self._two_block_street = []
        self._three_block_street = []
        self._block_list = [0 for x in range(40)]
        self._station_list = []
        self._utility_list = []
        self._corner_list = []
        self._chest_block_list = []
        self._chance_block_list = []
        self._tax_list = []
        self._player_dict = {}
        self._create_room_dict = create_room_dict
        self._players_list = self._create_room_dict["data"][0]["data"]
        self._game_setting = self._create_room_dict["data"][1]["data"]
        self._epic_bank = None
        self._street_color = OrderedDict()
        self._messager_handler = mess_hand
        self._block_position = []
        self.init_board()

    def _read_data(self):
        # generate a map
        parent_addr = os.path.abspath(os.pardir)
        self._block_list_data = json_reader(os.path.join(
            parent_addr, 'Data/block_data.json'))
        self._station_list_data = json_reader(os.path.join(
            parent_addr, 'Data/station_data.json'))
        self._utility_list_data = json_reader(os.path.join(
            parent_addr, 'Data/utility_data.json'))
        self._estate_list_data = json_reader(os.path.join(
            parent_addr, 'Data/estate_data.json'))
        self._chest_list_data = json_reader(os.path.join(
            parent_addr, 'Data/chest_data.json'))
        self._chance_list_data = json_reader(os.path.join(
            parent_addr, 'Data/chance_data.json'))
        self._bank_data = json_reader(
            os.path.join(parent_addr, 'Data/bank_data.json'))
        self._player_dict_data = json_reader(
            os.path.join(parent_addr, 'Data/player_list3.json'))

    def _init_player(self):
        # self._player_dict_data = self._player_dict_data["data"]
        # for i in range(len(self._player_dict_data)):
        #     p = player.Player(self._player_dict_data[i]['id'], self._player_dict_data[i]['name'], self._player_dict_data[i]['cash'],
        #                       self._player_dict_data[i]['alliance'])
        #     output_str = "{0} {1} {2} {3}".format(
        #         p.cash, p.id, p.name, p.alliance)
        #     print(output_str)
        #     self._player_dict[self._player_dict_data[i]['id']] = p
        self._player_dict_data = self._player_dict_data["data"]
        for i in range(len(self._players_list)):
            p = player.Player(self._players_list[i]['uid'], self._players_list[i]['name'], self._game_setting["init_fund"],
                              self._player_dict_data[i]['alliance'])
            output_str = "{0} {1} {2} {3}".format(
                p.cash, p.id, p.name, p.alliance)
            print(output_str)
            self._player_dict[self._player_dict_data[i]['id']] = p

    def _init_bank(self):
        if self._game_setting["is_limited"] is True:
            self._epic_bank = bank.Bank(
                '99', 'EpicBank', self._bank_data['data']['house_number'], self._bank_data['data']['hotel_number'])
        else:
            self._epic_bank = bank.Bank('99', 'EpicBank', 99, 99)

    def _init_block(self):
        for b in self._block_list_data["data"]:
            if b['block_type'] == 0:
                # ["Go", "Go to Jail", "In Jail", "Free Parking"]
                if b['name'] == "Go":
                    corner_block = block.Go(
                        b['name'], b['block_id'], b['position'], self._game_setting["go_salary"], b['description'])
                elif b['name'] == "Go to Jail":
                    corner_block = block.Go_To_Jail(
                        b['name'], b['block_id'], b['position'], b['description'])
                elif b['name'] == "In Jail":
                    corner_block = block.In_Jail(
                        b['name'], b['block_id'], b['position'], b['description'])
                elif b['name'] == "Free Parking":
                    corner_block = block.Free_Parking(
                        b['name'], b['block_id'], b['position'], b['description'])
                else:
                    pass
                self._block_list[corner_block.position] = corner_block
                self._corner_list.append(corner_block)
            elif b['name'] == "Community Chest":
                # "Community Chest"
                new_block = cardpile.Community_Chest(
                    b['name'], b['block_id'], b['position'], b['description'])
                self._block_list[new_block.position] = new_block
                self._chest_block_list.append(new_block)
            elif b['name'] == "Chance":  # "Chance"
                new_block = cardpile.Chance(
                    b['name'], b['block_id'], b['position'], b['description'])
                self._block_list[new_block.position] = new_block
                self._chance_block_list.append(new_block)
            elif b['block_type'] == 3:
                # ["Income Tax", "Super Tax"]
                if b['name'] == "Income Tax":
                    new_block = tax.Income_Tax(
                        b['name'], b['block_id'], b['position'], b['description'], 0.10)
                elif b['name'] == "Super Tax":
                    new_block = tax.Super_Tax(
                        b['name'], b['block_id'], b['position'], b['description'], 0.10)
                else:
                    pass
                self._block_list[new_block.position] = new_block
                self._tax_list.append(new_block)

    def _init_station(self):
        self._station_list = []
        # name, position, uid, estate_value, status, street_id
        for s in self._station_list_data["data"]:
            new_block = station.Station(
                s['name'], s['block_id'], s['position'], s['uid'], s['estate_value'], s['status'])
            self._station_list.append(new_block)
            self._block_list[new_block.position] = new_block
            self._epic_bank.add_asset(new_block)

    def _init_utility(self):
        self._utility_list = []
        # name, position, uid, estate_value, status, street_id
        for u in self._utility_list_data["data"]:
            new_block = utility.Utility(
                u['name'], u['block_id'], u['position'], u['uid'], u['estate_value'], u['status'])
            self._utility_list.append(new_block)
            self._block_list[new_block.position] = new_block
            self._epic_bank.add_asset(new_block)

    def _init_estate(self):
        self._estate_list = []
        for e in self._estate_list_data["data"]:
            new_block = estate.Estate(e['name'], e['block_id'], e['position'], e['uid'],
                                      e['estate_value'], e['status'], e['street_id'], e['house_value'])
            self._estate_list.append(new_block)
            self._block_list[new_block.position] = new_block
            self._epic_bank.add_asset(new_block)

    def _init_chest(self):
        # initialize chest cards
        self._chest_list = []
        for chest in self._chest_list_data["data"]:
            # 0: Collection, 1: Collect_from_players
            if chest['card_type'] == 0 or chest['card_type'] == 1:
                self._chest_list.append(card.CollectCard(chest['card_id'], chest['card_type'], chest['description'],
                                                         chest['amount']))
            elif chest['card_type'] == 2 or chest['card_type'] == 3:  # 2: Pay, 3: Pay_for_repair
                                                                    # or
                                                                    # chest['card_type']
                                                                    # == 8 8:
                                                                    # Pay_to_players
                self._chest_list.append(card.PayCard(chest['card_id'], chest['card_type'], chest['description'],
                                                     chest['amount']))
            # elif chest['card_type'] == 4 or chest['card_type'] == 6:  # 4: Move_indicate_position, 6: Move_nearby
            #     self._chest_list.append(card.MoveCard(chest['card_id'], chest['card_type'], chest['description'],
            #                                     chest['block_id']))
            # elif chest['card_type'] == 7:  # Move
            #     self._chest_list.append(card.MoveCard(chest['card_id'], chest['card_type'], chest['description'],
            #                                     chest['steps']))
            # elif chest['card_type'] == 5:  # Bailcard
            #     self._chest_list.append(card.BailCard(
            #         chest['card_id'], chest['card_type'], chest['description']))

    def _init_chance(self):
        # initialize chance cards
        self._chance_list = []
        for chance in self._chance_list_data["data"]:
            if chance['card_type'] == 0:  # 0: Collection
                                        # or chance['card_type'] == 1, 1:
                                        # Collect_from_players
                self._chance_list.append(card.CollectCard(chance['card_id'], chance['card_type'], chance['description'],
                                                          chance['amount']))
            elif chance['card_type'] == 2 or chance['card_type'] == 3 or chance['card_type'] == 8:  # 2: Pay,
                                                                                                    # 3: Pay_for_repair
                                                                                                    # 8:
                                                                                                    # Pay_to_players
                self._chance_list.append(card.PayCard(chance['card_id'], chance['card_type'], chance['description'],
                                                      chance['amount']))
            # 4: Move_indicate_position, 6: Move_nearby
            elif chance['card_type'] == 4 or chance['card_type'] == 6:
                self._chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                                       chance['block_id']))
            elif chance['card_type'] == 7:  # Move
                self._chance_list.append(card.MoveCard(chance['card_id'], chance['card_type'], chance['description'],
                                                       chance['steps']))
            # elif chance['card_type'] == 5:  # Bailcard
            #     self._chance_list.append(card.BailCard(
            #         chance['card_id'], chance['card_type'], chance['description']))

    def _init_block_street(self):
        # initialize chess board
        selected_colors = random.choice(
            [hex(c.value) for c in color.Color])
        for i in range(8):
            self._street_color[i] = selected_colors[i]
        self._two_block_street = []
        self._three_block_street = []
        for e in self._estate_list:
            if e.street_id == 1 or e.street_id == 8:
                self._two_block_street.append(e)
            else:
                self._three_block_street.append(e)

    def init_board(self):
        self._read_data()  # read data
        # init all the data
        self._init_bank()
        self._init_block()
        self._init_station()
        self._init_utility()
        self._init_estate()
        self._init_chest()
        self._init_chance()
        self._init_player()

    def get_data(self):
        data_dict = OrderedDict()
        data_dict['chess_board'] = self._block_list
        self.get_block_position()
        data_dict['player_dict'] = self._player_dict
        data_dict['epic_bank'] = self._epic_bank
        data_dict['chest_list'] = self._chest_list
        data_dict['chance_list'] = self._chance_list
        data_dict['station_list'] = self._station_list
        data_dict['utility_list'] = self._utility_list
        data_dict['estate_list'] = self._estate_list
        data_dict['corner_list'] = self._corner_list
        data_dict['chest_block_list'] = self._chest_block_list
        data_dict['chance_block_list'] = self._chance_block_list
        data_dict['tax_list'] = self._tax_list
        data_dict['street_color'] = self._street_color
        data_dict['msg'] = self._messager_handler
        difficulty = self._game_setting["level"]
        if difficulty == "easy":
            data_dict['ef'] = ef.EF(0.05)
        elif difficulty == "normal":
            data_dict['ef'] = ef.EF(0.10)
        else:
            data_dict['ef'] = ef.EF(0.15)
        return data_dict

    def new_board(self, data_dict):
        """
        Generate a new board
        :return: a board
        """
        two_block_street = copy.copy(self._two_block_street)
        three_block_street = copy.copy(self._three_block_street)
        station_list = copy.copy(self._station_list)
        utility_list = copy.copy(self._utility_list)
        corner_list = copy.copy(self._corner_list)
        chest_block_list = copy.copy(self._chest_block_list)
        chane_block_list = copy.copy(self._chance_block_list)
        tax_list = copy.copy(self._tax_list)

        two_block_street_1_index = [1, 3]
        two_block_street_8_index = [37, 39]
        three_block_street_2_index = [6, 8, 9]
        three_block_street_3_index = [11, 13, 14]
        three_block_street_4_index = [16, 18, 19]
        three_block_street_5_index = [21, 23, 24]
        three_block_street_6_index = [26, 27, 29]
        three_block_street_7_index = [31, 32, 34]
        stations_list_index = [5, 15, 25, 35]
        utility_list_index = [12, 28]
        # two_block_street
        random.shuffle(two_block_street_1_index)
        random.shuffle(two_block_street_8_index)
        two_block_street_index_all = [
            two_block_street_1_index, two_block_street_8_index]
        random.shuffle(two_block_street_index_all)
        self._two_block_street = reduce(
            lambda x, y: x + y, two_block_street_index_all)
        for i in self._two_block_street:
            self._block_list[i] = two_block_street.pop(0)
        # three_block_street
        random.shuffle(three_block_street_2_index)
        random.shuffle(three_block_street_3_index)
        random.shuffle(three_block_street_4_index)
        random.shuffle(three_block_street_5_index)
        random.shuffle(three_block_street_6_index)
        random.shuffle(three_block_street_7_index)
        three_block_street_index_all = [three_block_street_2_index, three_block_street_3_index,
                                        three_block_street_4_index, three_block_street_5_index, three_block_street_6_index, three_block_street_7_index]
        random.shuffle(three_block_street_index_all)
        self._three_block_street = reduce(
            lambda x, y: x + y, three_block_street_index_all)
        for j in self._three_block_street:
            self._block_list[j] = three_block_street.pop(0)
        # station
        random.shuffle(stations_list_index)
        self._station_list = stations_list_index
        for k in self._station_list:
            self._block_list[k] = station_list.pop(0)
        # utility
        random.shuffle(utility_list_index)
        self._utility_list = utility_list_index
        for p in self._utility_list:  # utility
            self._block_list[p] = utility_list.pop(0)

        data_dict['chess_board'] = self._block_list
        self.get_block_position()
        return data_dict

    def get_block(self, position):
        return self._block_list[position]

    def get_block_position(self):
        self._block_position = []
        for i in range(len(self._block_list)):
            self._block_position.append(self._block_list[i].position)

    def change_street_order(self):
        num_three_block_street = len(self._three_block_street)
        random_num = random.random()
        if random_num < 0.5:
            street_a = self._two_block_street[0]
            street_b = self._two_block_street[1]
            for index in range(2):
                block = street_a[index]
                temp = block.position
                block.position(street_b[index].position)
                street_b[index].position(temp)
            street_a.resort()
            street_b.resott()
        for i in range(3):
            int_a = random.randint(0, num_three_block_street)
            int_b = random.randint(0, num_three_block_street)
            while int_a == int_b:
                int_b = random.randint(0, num_three_block_street)
            street_a = self._three_block_street[int_a]
            street_b = self._three_block_street[int_b]
            self._change_two_street(street_a, street_b)
            street_a.resort()
            street_b.resort()

    def _change_two_street(self, street_a, street_b):
        for index in range(3):
            block = street_a[index]
            temp = block.position
            block.position(street_b[index].position)
            street_b[index].position(temp)

    # TODO: need to finish
    def getJSon(self):
        json_data = {
            "type": "board",
            "data": [
                {
                    "block_list": self._block_position
                }
            ]
        }
        return json_data
