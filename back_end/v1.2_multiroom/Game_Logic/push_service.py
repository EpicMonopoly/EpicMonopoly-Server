import json
import logging
import multiprocessing

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line

# import game_entrance
import room_detail

# import threading

rooms = dict()

# game push methods


def push2all_r(line, roomid, conn):
    # print(roomid, ":2p:", line)
    conn.send((roomid, line))
    # to parentconn in room_detail listener


def wait_choice_r(roomid, conn):
    # child to recv
    print("wait_choice:", roomid)
    iroomid, line = conn.recv()
    assert (iroomid == roomid)
    while line == -1:
        iroomid, line = conn.recv()
        assert (iroomid == roomid)
    return line


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class MywebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.roomid = self.get_argument("roomid")
        self.stream.set_nodelay(True)
        if self.roomid in rooms:
            rooms[self.roomid].add_clients(self.id, self)
        else:
            rooms[self.roomid] = room_detail.Room_detail(
                self.roomid, (self.id, self))

    def on_message(self, message):
        try:
            data = json.loads(message)
            if data['request'] == 'uid':
                logging.info("Room %s Client %s sent a json : %s " %
                             (self.roomid, self.id, data))
                rooms[self.roomid].get_client(
                    self.id).write_message("Your id is " + self.id)
                data = {"type": "json",
                        "response": "This is response for trying to get uid."}
                rooms[self.roomid].get_client(self.id).write_message(data)
        except (ValueError, TypeError) as err:
            if message == "<recall>":
                single_push(self.roomid, self.id)
                return
            logging.info("Room %s Client %s sent a message : %s " %
                         (self.roomid, self.id, message))
            rooms[self.roomid].global_Choice.set_choice(message)
            rooms[self.roomid].sender(message)
            rooms[self.roomid].add_log(self.id, message)
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


app = tornado.web.Application({
    (r"/", IndexHandler),
    (r"/websocket", MywebSocketHandler),
})


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
