import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

def runserver(apps):
    
    define('port', default=8080, help='run on given port', type=int)

    httpServer = tornado.httpserver.HTTPServer(App(apps))

    httpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("sup, world")


class App(tornado.web.Application):
    '''
    Tornado server class.
    '''
    def __init__(self,apps):

        self.apps = apps

        self.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        
        handlers = []

        for app in self.apps:
            for route in self.apps[app]['routes']:
                handlers.append((r"%s" % route, MainHandler))
               




        tornado.web.Application.__init__(self, handlers, **self.settings)


