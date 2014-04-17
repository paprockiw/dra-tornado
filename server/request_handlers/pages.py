"""
This is the request handler for pages.
It should only allow get and disable post and put
"""

import json

import tornado.web
import tornado.gen

import document

# import pdb

class RequestHandler(document.RequestHandler):

    @tornado.web.asynchronous
    def post(self, param):
        """ 
        Gets document based on path. 
        """
        
        self.return_error('hay stop trying to hack me')

    @tornado.web.asynchronous
    def put(self, param):
        """ 
        Gets document based on path. 
        """
        
        self.return_error('hay stop trying to hack me')



        



