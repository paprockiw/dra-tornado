"""
module for setting up the tornado app for our project
"""

# use to dynamical import modules
from importlib import import_module

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import apps

import pdb


def run():
    """
    run tornado server
    """

    
    define('port', default=8080, help='run on given port', type=int)

    routes = []

    def route_not_found(route,routes):
        """
        returns True if route was not found in routes
        """

        for item in routes:
            if item[0] == route:
                return False
       
        return True

    for app in apps.apps:
        if 'routes' in apps.apps[app]:
            for key, value in apps.apps[app]['routes'].iteritems():
                if route_not_found(key, routes):
                    routes.append((r"%s" % key, import_module(value['requestHandler'])))

    
    app = tornado.web.Application(routes)

    app.settings = {
        'cookie_secret': 'swipetechnologies'
    }

    httpServer = tornado.httpserver.HTTPServer(app)

    httpServer.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

    



