"""
This is the request handler makes sure that secure login cookie 
is present before geting or posting to the request handler
"""

import json

import tornado.web
import tornado.gen

import document

import pdb

class RequestHandler(document.RequestHandler):

    @tornado.web.asynchronous
    def prepare(self):
        """
        befor request handler handles any request it must go through this method
        """

        ### check to see if secure cookie login is present ###

        # pdb.set_trace()
        
        login = self.get_secure_cookie("login")

        if login == None:
            self.custom_error_response('needs login cookie')



        



