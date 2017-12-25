import threading
import json


class messenger:

    def __init__(self, room_id, msg_tunnel):
        self._room_id = room_id
        self._msg_tunnel = msg_tunnel
        self._msg_queue = []
        self._t = threading.Thread(target=self._monitor)
        self._t.start()
        self._stop_flag = False

    @property
    def msg_queue(self):
        return self._msg_queue

    def _monitor(self):
        while(self._stop_flag is False):
            self.wait_choice()

    def _add_new_player(self, player_info):
        import player
        import main
        p = player.Player(player_info["id"], player_info["name"], 2000, "America")
        main.add_player(p)

    def join_thread(self):
        self._stop_flag = True
        self._t.join()

    def push2all(self, line):
        # print(roomid, ":2p:", line)
        self._msg_tunnel.send((self._room_id, line))
        # to parentconn in room_detail listener

    def wait_choice(self):
        # child to recv
        print("wait_choice:", self._room_id)
        iroomid, line = self._msg_tunnel.recv()
        assert (iroomid == self._room_id)
        while line == -1:
            iroomid, line = self._msg_tunnel.recv()
            assert (iroomid == self._room_id)
        json_obj = json.loads(line)
        if json_obj["type"] == "new_player":
            self._add_new_player(json_obj["data"][0])
        else:
            self._msg_queue.append(json_obj)


if __name__ == "__main__":
    m = messenger(12, "a")
    m.join_thread()
