import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

def runserver():
    define('port', default=8080, help='run on given port', type=int)
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("sup, world")


class App(tornado.web.Application):
    '''
    Tornado server class.
    '''
    def __init__(self):
        settings = {'cookie_secret': 'swipetechnologies'}
        # add code that takes the routes set up in apps and adds them to the 
        # array as tuples here:
        handlers = [(r'/', MainHandler),]
        tornado.web.Application.__init__(self, handlers, **settings)


