"""
This is the request handler incharge pages
"""

import json

import tornado.web
import tornado.gen

import document

import pdb

class RequestHandler(document.RequestHandler):

    @tornado.web.asynchronous
    def prepare(self):

        login = self.get_secure_cookie("login")

        if login == None:
            self.return_error('needs login cookie')



        



