from tornado.ioloop import IOLoop

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/?", MainHandler)]
        tornado.web.Application.__init__(self, handlers)


if __name__ == '__main__':
    app = Application()
    app.listen(8000)
    IOLoop.instance().start()
