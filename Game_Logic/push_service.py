import json
import logging
import multiprocessing
import os
import uuid

import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line

import room_detail

rooms = dict()
wait_room = dict()
room_id_counter = 100

in_game_room = dict()


def get_roomid():
    global room_id_counter
    room_id_counter += 1
    return room_id_counter - 1


class gameHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("login_page.html")


class InGameHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("in_game.html")


class InitRoomHanler(tornado.web.RequestHandler):
    global wait_room

    def post(self):
        print(self.request.body)
        if self.request.body:
            try:
                json_data = tornado.escape.json_decode(self.request.body)
                print("json_data", json_data)

                for dat in json_data["data"]:
                    if "type" in dat:
                        if dat["type"] == "player":
                            dat["data"][0]["uid"] = str(uuid.uuid1())
                        elif dat["type"] == "room":
                            dat["data"][0]["room_id"] = str(get_roomid())
                print("response", json_data)

                for dat in json_data["data"]:
                    if "type" in dat:
                        if dat["type"] == "room":
                            room_config = dat["data"][0]
                            roomid = room_config["room_id"]
                            break
                    else:
                        roomid = dat["room_id"]

                for dat in json_data["data"]:
                    if "type" in dat:
                        if dat["type"] == "player":
                            player_detail = dat["data"][0]
                            break

                if roomid not in wait_room:
                    wait_room[roomid] = {
                        "room": room_config,
                        "player_list": []
                    }
                wait_room[roomid]["player_list"].append(player_detail)
                self.write(tornado.escape.json_encode(json_data))
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request


class RoomlistHanler(tornado.web.RequestHandler):
    global wait_room

    def get(self):
        self.write(tornado.escape.json_encode(wait_room))


class StartGametHanler(tornado.web.RequestHandler):
    global wait_room

    def post(self):
        roomid = self.get_argument("roomid")
        if len(wait_room[roomid]["player_list"]) > 1:
            response = {"start": True}
            self.write(tornado.escape.json_encode(response))
        else:
            response = {"start": False}
            self.write(tornado.escape.json_encode(response))


class MywebSocketHandler(tornado.websocket.WebSocketHandler):
    global wait_room, in_game_room, rooms

    def open(self, *args):
        self.id = self.get_argument("Id")
        self.roomid = self.get_argument("roomid")

        if self.roomid not in in_game_room:
            in_game_room[self.roomid] = {}
        in_game_room[self.roomid][self.id] = self

        if len(in_game_room[self.roomid]) == len(wait_room[self.roomid]):
            rooms[self.roomid] = room_detail.Room_detail(self.roomid,
                                                         wait_room[self.roomid], in_game_room[self.roomid])

        self.stream.set_nodelay(True)
        # if self.roomid in rooms:
        #     # 新玩家加入
        #     rooms[self.roomid].add_clients(self.id, self)
        #     self.write_message("<NEW_PLAYER-S>")
        # else:
        #     # 创建新房间
        #     rooms[self.roomid] = room_detail.Room_detail(
        #         self.roomid, (self.id, self))
        #     self.write_message("<NEW_PLAYER-O>")

    def on_message(self, message):
        print(message)
        try:
            data = json.loads(message)
            # rooms[self.roomid].mess_hand.msg_queue.append(data)
            if data['type'] == 'input':
                input_data = data["data"][0]
                assert(input_data["from_player_id"] == self.id)
                logging.info("Room %s Client %s sent a message : %s " %
                             (self.roomid, self.id, input_data["request"]))
                rooms[self.roomid].sender(message)
                # rooms[self.roomid].sender(input_data["request"])
                rooms[self.roomid].global_Choice.set_choice(
                    input_data["request"])
                rooms[self.roomid].add_log(self.id, input_data["request"])
        except (ValueError, TypeError) as err:
            if message == "<recall>":
                single_push(self.roomid, self.id)
                return
            logging.error("This is not json.")

    def on_close(self):
        if self.id in rooms[self.roomid].clients:
            rooms[self.roomid].rm_clients(self.id)
            if not rooms[self.roomid].clients:
                del rooms[self.roomid]
                logging.info("Room %s is closed." %
                             (self.roomid))
            logging.info("Room %s Client %s is closed." %
                         (self.roomid, self.id))

    def check_origin(self, origin):
        return True


app = tornado.web.Application(
    [
        (r"/", IndexHandler),
        (r"/joingame", InitRoomHanler),
        (r"/ingame", InGameHandler),
        (r"/roomlist", RoomlistHanler),
        (r"/start", StartGametHanler),
        (r"/game", gameHandler),
        (r"/websocket", MywebSocketHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


# def push():
#     while True:
#         roomid = input("Room to push:")
#         server_input = input("Force push:")
#         if roomid in rooms:
#             for key in rooms[roomid].clients.keys():
#                 rooms[roomid].get_client(key).write_message(server_input)
#                 logging.info("Write to Room %s client %s: %s" %
#                              (roomid, key, server_input))
#         else:
#             logging.error("This roodid don not exisit.")


def single_push(roomid, id):
    if roomid in rooms:
        room = rooms[roomid]
        for i in range(len(room.game_log)):
            room.clients[id]["object"].write_message(room.game_log[i][1])
            logging.info("Write to Room %s client %s: %s" %
                         (roomid, id, room.game_log[i][1]))
    else:
        logging.error("This roodid don not exisit.")


def main():
    # threading.Thread(target=push).start()
    define("port", default=8888, help="run on the given port", type=int)
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
