"""
module for setting up the tornado app for our project
"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options


def run_server(apps):
    """
    run tornado server
    """
    
    define('port', default=8080, help='run on given port', type=int)

    httpServer = tornado.httpserver.HTTPServer(App(apps))

    httpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



class App(tornado.web.Application):
    """
    class for setting up tornado app
    """
    
    def __init__(self, apps):

        self.apps = apps

        self.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        ### setup handlers for our apps ### 

        self.handlers = []

        for app in self.apps:
            if 'routes' in self.apps[app]:
                for route in self.apps[app]['routes']:
                    self.handlers.append(( r"%s" % route, eval(self.apps[app]['routes'][route]['request_handler']) ))      

        tornado.web.Application.__init__(self, self.handlers, **self.settings)



class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Login")


class DocumentHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Document")




