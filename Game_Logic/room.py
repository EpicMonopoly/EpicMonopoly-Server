import board
import bank

WAIT = 1
START = 2
END = 3


class Room:

    def __init__(self, room_id, board, bank):
        """
        Constructor
        :type room_id: int
        :type board: board.Board
        :type bank: bank.Bank
        :param room_id: room id
        :param board: board we generated
        :param bank: bank we instanced
        """
        self._room_id = room_id
        self._status = WAIT  # default status for room
        self._board = board
        self._bank = bank
        self._player_list = []

    def add_player(self, player):
        self._player_list.append(player)

    @property
    def bank(self):
        return self.bank

    @property
    def room_id(self):
        return self._room_id

    @property
    def board(self):
        return self._board

    @property
    def players(self):
        return self._player_list

    def leave(self, player):
        self._player_list.remove(player)





