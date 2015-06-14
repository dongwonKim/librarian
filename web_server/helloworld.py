#!/usr/bin/python

import tornado.httpserver
import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("helloworld.html",title="Seat")

settings = {
	"static_path":os.path.join(os.path.dirname(__file__),"static"),
}

application = tornado.web.Application([
	(r"/",MainHandler),
	(r"/static/$", tornado.web.StaticFileHandler, {'path': "static_path"}),
], **settings)


if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8889)
	tornado.ioloop.IOLoop.instance().start()
