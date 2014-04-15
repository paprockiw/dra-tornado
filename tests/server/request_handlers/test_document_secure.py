import sys
import json

import unittest

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none


import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

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


    def test1(self):
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


    def test2(self):
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

        # set cookie
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

        # set phony cookie
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


    def test3(self):
        """
        if secure cookie is present then it should be able to post to request handler
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/login/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'username':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        headers = tornado.httputil.HTTPHeaders({"content-type": "text/html"})

        # set cookie
        headers.add("Cookie", response.headers['Set-Cookie'])

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/users'),\
            method="POST",\
            headers=headers,\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)

        ## confirm is data was saved ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/users'),\
            headers=headers,\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        users = json.loads(response.body)

        assert_equals(users['administrator'],'admin-test')
        assert_equals(users['password'],'swipe-test')


        # set data back
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/users'),\
            method="POST",\
            headers=headers,\
            body=json.dumps({ 'administrator':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        # confirm
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document-secure/admin/administrator/users'),\
            headers=headers,\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        users = json.loads(response.body)

        assert_equals(users['administrator'],'admin')
        assert_equals(users['password'],'swipe')









    
