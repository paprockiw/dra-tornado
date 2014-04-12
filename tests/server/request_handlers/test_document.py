import sys
import json

import unittest

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none


import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from server.request_handlers import document

import pdb

 
class Login(AsyncHTTPTestCase):

    def get_app(self):
        """
        setup tornado application for this test
        """


        app = Application([(r'/document/(.+)', document.RequestHandler)])

        app.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        return app


    def test_case1(self):
        """
        it should return a json if correct path was given
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()


        data = json.loads(response.body)


        assert_equals(type(data),dict)
        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


    def test_case2(self):
        """
        it should return a error if wrong path was given
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/wrong/path'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.body,'tornado threw an exception')

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error)


    def test_case3(self):
        """
        it should save data based on path
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)

        ## confirm is data was saved ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        users = json.loads(response.body)

        assert_equals(users['administrator'],'admin-test')
        assert_equals(users['password'],'swipe-test')


        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        users = json.loads(response.body)

        assert_equals(users['administrator'],'admin')
        assert_equals(users['password'],'swipe')


        






