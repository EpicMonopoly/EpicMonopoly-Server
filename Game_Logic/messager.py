import threading
import json


class Messager(object):

    def __init__(self, room_id, msg_tunnel):
        self._room_id = room_id
        self._msg_tunnel = msg_tunnel
        self._msg_queue = []
        self._flag = False
        self._t = threading.Thread(target=self._monitor)
        self._t.start()

    @property
    def msg_queue(self):
        return self._msg_queue

    def _monitor(self):
        """
        A threading keep apply wait_choice function
        """
        while not self._flag:
            self.wait_choice()

    def _add_new_player(self, player_info):
        """
        Add new player if exist
        """
        import player
        import game_entrance
        p = player.Player(player_info["id"],
                          player_info["name"], 2000, "America", [3, 6])
        game_entrance.add_player(p)

    # def join_thread(self):
    #     self._flag = True
    #     self._t.join()

    def push2single(self, uid, line):
        """
        Push line to player who id is uid

        Parameters
        ----------
        self: 
        uid: id of player
        line: str

        """
        self._msg_tunnel.send((self._room_id, line, uid))
        print("M:Push to Room {}@{} {}".format(self._room_id, uid, line))

    def push2all(self, line):
        """
        Push line to all player
        """
        self._msg_tunnel.send((self._room_id, line, "ALL"))
        print("M:Push to Room {}@ALL {}".format(self._room_id, line))
        # to parentconn in room_detail listener

    def wait_choice(self):
        """
        wait player's input
        """
        # child to recv
        print("Room {} wait choice:".format(self._room_id))
        iroomid, line = self._msg_tunnel.recv()
        print("line", line)
        assert (iroomid == self._room_id)
        while line == -1:
            iroomid, line = self._msg_tunnel.recv()
            assert (iroomid == self._room_id)
        json_obj = json.loads(line)
        if json_obj["type"] == "new_player":
            self._add_new_player(json_obj["data"][0])
        else:
            self._msg_queue.append(json_obj)
        # print(self._msg_queue)

    def get_json_data(self, key_word):
        """
        Return json data according to key word
        """
        for i in range(len(self._msg_queue)):
            if self._msg_queue[i]["type"] == key_word:
                temp = self._msg_queue[i]
                del self._msg_queue[i]
                return temp["data"]
        return False


if __name__ == "__main__":
    m = Messager(12, "a")
    # m.join_thread()
