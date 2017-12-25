import random
import copy
from functools import reduce

class Board:
    """
    Board class
    """
    def __init__(self, two_block_street, three_block_street, station_list, utility_list, block_list,
                 corner_list, chest_block_list, chance_block_list, tax_list):
        """
        Initialize the board
        :param two_block_street: list
        :param three_block_street: list
        :param block_list: list
        :param station_list: list
        :param utility_list: list
        """
        self._two_block_street = two_block_street
        self._three_block_street = three_block_street
        self._station_list = station_list
        self._utility_list = utility_list
        self._block_list = block_list
        self._corner_list = corner_list
        self._chest_block_list = chest_block_list
        self._chance_block_list = chance_block_list
        self._tax_list = tax_list

    
    def new_board(self, chess_board_dict):
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
        two_block_street_index_all = [two_block_street_1_index, two_block_street_8_index]
        random.shuffle(two_block_street_index_all)
        self._two_block_street = reduce(lambda x, y: x + y, two_block_street_index_all)
        for i in self._two_block_street:  
            chess_board_dict[i] = two_block_street.pop(0)
        # three_block_street
        random.shuffle(three_block_street_2_index)
        random.shuffle(three_block_street_3_index)
        random.shuffle(three_block_street_4_index)
        random.shuffle(three_block_street_5_index)
        random.shuffle(three_block_street_6_index)
        random.shuffle(three_block_street_7_index)
        three_block_street_index_all = [three_block_street_2_index, three_block_street_3_index, three_block_street_4_index, three_block_street_5_index, three_block_street_6_index, three_block_street_7_index]
        random.shuffle(three_block_street_index_all)
        self._three_block_street = reduce(lambda x, y: x + y, three_block_street_index_all)
        for j in self._three_block_street:
            chess_board_dict[j] = three_block_street.pop(0)
        # station
        random.shuffle(stations_list_index)
        self._station_list = stations_list_index
        for k in self._station_list: 
            chess_board_dict[k] = station_list.pop(0)
        # utility
        random.shuffle(utility_list_index)
        self._utility_list = utility_list_index
        for p in self._utility_list:  # utility
            chess_board_dict[p] = utility_list.pop(0)
     
        chess_board = []
        for i in range(40):
            chess_board.append(chess_board_dict[i])
        return chess_board

    def get_block(self, position):
        return self._block_list[position]

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

    #TODO: need to finish
    def getJSon(self):
        pass





