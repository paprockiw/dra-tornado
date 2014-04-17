"""
test document request handler
"""

import sys
import json

import unittest

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none


import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from server.request_handlers import pages

import pdb

 
class Pages(AsyncHTTPTestCase):

    def get_app(self):
        """
        setup tornado application for this test
        """

        app = Application([
            (r'/pages/(.+)', pages.RequestHandler)
        ])

        return app


    def test1(self):
        """
        it should return a json if correct path was given
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/pages/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(type(data),dict)
        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


    def test2(self):
        """
        it should return a error if wrong path was given
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/pages/admin/administrator/wrong/path'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.body,'tornado threw an exception')

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error)



    def test3(self):
        """
        it should return an error if I try to post
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/pages/admin/administrator/pages'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error) 
        assert_equals(response.body,'hay stop trying to hack me')

    
    def test4(self):
        """
        it should return an error if I try to put
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/pages/admin/administrator/pages'),\
            method="PUT",\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error) 
        assert_equals(response.body,'hay stop trying to hack me')

    