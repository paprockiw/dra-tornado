import json

import tornado.web
import tornado.gen
import tornado.httpclient

# import pdb


class RequestHandler(tornado.web.RequestHandler):

    connections = {}

    @tornado.web.asynchronous
    def get(self, key):  
        RequestHandler.connections.setdefault(key,[]).append(self.callback) 

    def callback(self):
        self.finish()


    @tornado.web.asynchronous
    def post(self, key):

        if RequestHandler.connections.get(key):
            for callback in RequestHandler.connections[key]:
                callback()

            del RequestHandler.connections[key]

        self.finish()

            