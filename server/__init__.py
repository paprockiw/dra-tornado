"""
module for setting up the tornado app for our project
"""

## system imports ##
import os, sys
from importlib import import_module # use to dynamical import modules
# import pdb

## third party import ##
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

## project modules ##
import apps


sys.path.insert(0, os.path.abspath(''))


def run():
    """
    run tornado server
    """

    def route_not_found(route,routes):
        """
        returns True if route was not found in routes
        """

        for _route in routes:

            # route was found
            if _route[0] == route:
                return False
       
        # no routes were found
        return True

    ## setup routes ##

    routes = []

    for app in apps.apps:

        # if app has routes
        if 'routes' in apps.apps[app]:

            # loop through all the routes
            for key, val in apps.apps[app]['routes'].iteritems():

                # if route not found 
                if route_not_found(key, routes):

                    # then append route to routes
                    routes.append((r"%s" % key, import_module(val).RequestHandler))

    
    ## run app ##

    define('port', default=8080, help='run on given port', type=int)

    app = tornado.web.Application(routes)

    app.settings = {
        'cookie_secret': 'swipetechnologies'
    }

    httpServer = tornado.httpserver.HTTPServer(app)

    httpServer.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

    



