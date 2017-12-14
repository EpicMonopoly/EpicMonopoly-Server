import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import json

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

clients = dict()


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class MywebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        try:
            data = json.loads(message)
            logging.info("Client %s sent a message : %s " % (self.id, data))
            if data['request'] == 'uid':
                clients[self.id]["object"].write_message("Your id is " + self.id)
                # json传输给客户端，直接传入字典即可
                data = {"type": "json", "response": "This is response for trying to get uid."}
                clients[self.id]["object"].write_message(data)

        except ValueError:
            logging.info("Client %s sent a message : %s " % (self.id, message))
            logging.error("This is not json.")

    def on_close(self):
        if self.id in clients:
            del clients[self.id]
            print("Client %s is closed." % (self.id))

    def check_origin(self, origin):
        return True


app = tornado.web.Application({
    (r"/", IndexHandler),
    (r"/websocket", MywebSocketHandler),
})

import threading
import time


def sendTime():
    import datetime
    while True:
        for key in clients.keys():
            msg = str(datetime.datetime.now())
            clients[key]["object"].write_message(msg)
            print("Write to client %s: %s" % (key, msg))
        time.sleep(1)


def push():
    while True:
        server_input = input("Force push:")
        for key in clients.keys():
            clients[key]["object"].write_message(server_input)
            print("Write to client %s: %s" % (key, server_input))


if __name__ == "__main__":
    threading.Thread(target=push).start()
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
