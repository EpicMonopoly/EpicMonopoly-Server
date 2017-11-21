import os
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)


class initHandler(tornado.web.RequestHandler):
    def get(self):
        part = self.get_argument('init')
        if part == '' or None:
            self.set_status(404)
            return None
        else:
            dir = os.path.abspath(os.curdir)
            print("------{}------".format(dir))
            file = "Data/" + part + ".json"
            fulldirfile = os.path.join(dir, file)
            print("------{}------".format(fulldirfile))
            if not os.path.isfile(fulldirfile):
                self.set_status(404)
                return None
            else:
                with open(fulldirfile, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.write(data)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", initHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

