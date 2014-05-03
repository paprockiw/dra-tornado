"""
test document request handler

needs admin database setup inorder for tests to work
"""

## system imports ##

import sys
import json
import unittest
import mock

import pdb


## third party import ##

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none

import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application


## project imports ##

from server.request_handlers import document



 
class Document(AsyncHTTPTestCase):
    """
    this is the request handler for reteiving and saving data to 
    any document in a database, based on path
    """

    def get_app(self):
        """
        setup tornado application for this test
        """

        app = Application([
            (r'/document/(.+)', document.RequestHandler)
        ])

        app.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        return app


    def test1(self):
        """
        it should return a json if correct path was given
        """

        ### make requset ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        ### test response ###

        data = json.loads(response.body)

        # response is a json
        assert_equals(type(data), dict)

        # response is okay
        assert_equals(response.reason, 'OK')

        # there where no errors
        assert_is_none(response.error)

        


    def test2(self):
        """
        it should return a error if wrong path was given
        """

        ### make requset ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/wrong/path'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()


        ### test response ###

        # it should return this messsage
        assert_equals(response.body,'tornado threw an exception')

        # reason shold be Bad Request
        assert_equals(response.reason,'Bad Request')

        # there where errors
        assert_is_not_none(response.error)


    def test3(self):
        """
        it should save data based on path
        """

        ### make requset ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        ### test response ###

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)

        ## confirm is data was saved ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['resp']['administrator'],'admin-test')
        assert_equals(data['resp']['password'],'swipe-test')


        ## set data back ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ## confirm that data was setback ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['resp']['administrator'],'admin')
        assert_equals(data['resp']['password'],'swipe')


    def test4(self):
        """
        when ever we do a get we should cached it to redis,
        if it's not in cached get data from couchdb and then
        cached it to redis
        """

        ### make requset ###

        # this should clear cache if there was one 
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin-test', 'password':'swipe-test' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()


        ## confirm that cache was cleared ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cached'], False)


        ## call it again and this time it should be true ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cached'], True)


        ## if I do a post then it should clear the cache ##

        # this should clear cache if there was one 
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'administrator':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()


        ## confirm that cache was cleared ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/users'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cached'], False)

        


        






