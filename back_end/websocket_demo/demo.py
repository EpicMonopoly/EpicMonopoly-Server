import tornado.ioloop
import tornado.web
import tornado.websocket
import logging

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
        logging.info("Client %s received a message : %s " % (self.id, message))

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
