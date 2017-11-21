import random
import copy

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

    def new_board(self):
        """
        Generate a new board
        :return: a board
        """
        chess_board_dict = {}
        # for 
        # two_block_street = copy.copy(self._two_block_street)
        # three_block_street = copy.copy(self._three_block_street)
        # station_list = copy.copy(self._station_list)
        # utility_list = copy.copy(self._utility_list)
        # corner_list = copy.copy(self._corner_list)
        # chest_block_list = copy.copy(self._chest_block_list)
        # chane_block_list = copy.copy(self._chance_block_list)
        # tax_list = copy.copy(self._tax_list)

        # for i in (1, 3, 37, 39):  # two_block_street
        #     chess_board_dict[i] = two_block_street.pop()
        # for j in (6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34):
        #     chess_board_dict[j] = three_block_street.pop()
        # for k in (5, 15, 25, 35):  # station
        #     chess_board_dict[k] = station_list.pop()
        # for p in utility_list:  # utility
        #     if p.name == "Power Station":
        #         chess_board_dict[12] = p
        #         utility_list.remove(p)
        #     elif p.name == "Water Work":
        #         chess_board_dict[28] = p
        #         utility_list.remove(p)
        # for l in corner_list:
        #     if l.name == "Go":    # "Go"
        #         chess_board_dict[0] = l
        #         corner_list.remove(l)
        #     elif l.name == "Go to Jail":  # "Go to Jail"
        #         chess_board_dict[30] = l
        #         corner_list.remove(l)
        #     elif l.name == "In Jail":  # "In Jail"
        #         chess_board_dict[10] = l
        #         corner_list.remove(l)
        #     elif l.name == "Free Parking":  # "Free Parking"
        #         chess_board_dict[20] = l
        #         corner_list.remove(l)
        # for q in chest_block_list:
        #     if q.name == "Community Chest" and 2 not in chess_board_dict:  # "Community Chest"
        #         chess_board_dict[2] = q
        #         chest_block_list.remove(q)
        #     elif q.name == "Community Chest" and 17 not in chess_board_dict:  # "Community Chest"
        #         chess_board_dict[17] = q
        #         chest_block_list.remove(q)
        #     elif q.name == "Community Chest" and 33 not in chess_board_dict:  # "Community Chest"
        #         chess_board_dict[33] = q
        #         chest_block_list.remove(q)
        # for r in chane_block_list:
        #     if r.name == "Chance" and 7 not in chess_board_dict:  # "Chance"
        #         chess_board_dict[7] = r
        #         chest_block_list.remove(r)
        #     elif q.name == "Chance" and 22 not in chess_board_dict:  # "Chance"
        #         chess_board_dict[22] = r
        #         chest_block_list.remove(r)
        #     elif q.name == "Chance" and 36 not in chess_board_dict:  # "Chance"
        #         chess_board_dict[36] = r
        #         chest_block_list.remove(r)
        # for s in tax_list:
        #     if s.name == "Income Tax":
        #         chess_board_dict[4] = s
        #         tax_list.remove(s)
        #     elif s.name == "Super Tax":
        #         chess_board_dict[38] = s
        #         tax_list.remove(s)
        # chess_board = []
        # for i in range(40):
        #     chess_board.append(chess_board_dict[i])
        # return chess_board

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
            int_a = random.randint(num_three_block_street)
            int_b = random.randint(num_three_block_street)
            while int_a == int_b:
                int_b = random.randint(num_three_block_street)
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







