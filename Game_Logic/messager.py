import threading
import json


class Messager:

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
        while not self._flag:
            self.wait_choice()

    def _add_new_player(self, player_info):
        import player
        import game_entrance
        p = player.Player(player_info["id"],
                          player_info["name"], 2000, "America", player_info['avatar'])
        game_entrance.add_player(p)

    # def join_thread(self):
    #     self._flag = True
    #     self._t.join()

    def push2single(self, uid, line):
        """
        push message to single player

        """
        self._msg_tunnel.send((self._room_id, line, uid))
        print("M:Push to Room {}@{} {}".format(self._room_id, uid, line))

    def push2all(self, line):
        """
        push message to all players
        """
        # print(roomid, ":2p:", line)
        self._msg_tunnel.send((self._room_id, line, "ALL"))
        print("M:Push to Room {}@ALL {}".format(self._room_id, line))
        # to parentconn in room_detail listener

    def wait_choice(self):
        """
        wait for choice
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
        # print("queue", self._msg_queue, key_word)
        for i in range(len(self._msg_queue)):
            # print(key_word, self._msg_queue[i]["type"])
            if self._msg_queue[i]["type"] == key_word:
                temp = self._msg_queue[i]
                del self._msg_queue[i]
                return temp["data"]
        return False


if __name__ == "__main__":
    m = Messager(12, "a")
    # m.join_thread()
