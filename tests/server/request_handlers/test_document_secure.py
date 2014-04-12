import os
import sys
import json

import unittest

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none


import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

# add to sys.path
path = os.path.realpath(os.path.realpath(__file__) + '/../../../../fabfile/')
sys.path.append(path)

from server.request_handlers import document_secure, login

import pdb

 
class Pages(AsyncHTTPTestCase):

    def get_app(self):
        """
        setup tornado application for this test
        """


        app = Application([
            (r'/login/(.+)', login.RequestHandler),
            (r'/document-secure/(.+)', document_secure.RequestHandler)
        ])

        app.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        return app


    def test_1(self):
        """
        it should return a an error if login cookie is not present
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_equals(response.body,'needs login cookie')


    def test_2(self):
        """
        if login cookie is present then it should be able to get data
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/login/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'username':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        headers = tornado.httputil.HTTPHeaders({"content-type": "text/html"})

        # phony value
        headers.add("Cookie", response.headers['Set-Cookie'])

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/pages'),\
            method="GET",
            headers=headers
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')

        headers = tornado.httputil.HTTPHeaders({"content-type": "text/html"})

        # phony value
        headers.add("Cookie", 'login="dHJ1ZQ==|1397172234|4c3f413903148b7c71c9049c465318bc1ce1234"; Path=/')

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/pages'),\
            method="GET",
            headers=headers
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_equals(response.body,'needs login cookie')









    