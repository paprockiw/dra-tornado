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
        it should return a data if a valid path was given
        """

        ### make requset with a vaild path ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        # wait for response
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        # get data
        data = json.loads(response.body)

        # response is a json
        assert_equals(type(data), dict)
        assert_is_not_none(data['resp'])
        assert_is_not_none(data['cache'])

        # response is okay
        assert_equals(response.reason, 'OK')

        # there where no errors
        assert_is_none(response.error)

        


    def test2(self):
        """
        it should return a error if an invalid path was given
        """

        ### make requset with invalid path ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/invalid/path'),\
            method="GET",
            )

        # wait for response
        self.http_client.fetch(request, self.stop)
        response = self.wait()


        # reason shold be Bad Request
        assert_equals(response.reason,'Bad Request')

        # there where errors
        assert_is_not_none(response.error)

        # it should return this error messsage
        assert_equals(response.body,'tornado threw an exception')

        

    def test3(self):
        """
        it should save data based on path
        """

        ### save original data ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        originalData = json.loads(response.body)

        assert_equals(type(originalData), dict)


        ### update new data ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="POST",\
            body=json.dumps({ "pages": [{ "title": "page1" }, { "title": "page2" }, { "title": "page3" }] })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)

        
        ### confirm if data was saved ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['resp']['pages'][0]['title'], 'page1')
        assert_equals(data['resp']['pages'][1]['title'], 'page2')
        assert_equals(data['resp']['pages'][2]['title'], 'page3')


        ### set original data back ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="POST",\
            body=json.dumps(originalData['resp'])\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ### confirm that data was setback ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['resp'], originalData['resp'])

        


    def test4(self):
        """
        when ever we do a get we should get it from the redis cache,
        if it's not in the cache get data from couchdb and then
        cache it to redis
        """


        ### call url first time ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ## call it again and this time it should be pulling from cache ##

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cache'], True)


    


    def test5(self):
        """
        when ever we do a post, we should clear the redis cache
        """

        ### save original data ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        originalData = json.loads(response.body)

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ### clear cache ###

        # this should clear cache if there was one 
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="POST",\
            body=json.dumps({ "pages": [{ "title": "page1" }, { "title": "page2" }, { "title": "page3" }] })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ### do a get and this time cache should be False ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cache'], False)


        ### do it again and this time cache should be True ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cache'], True)


        ### restor data  ###

        # this should clear cache if there was one 
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="POST",\
            body=json.dumps(originalData['resp'])\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)


        ### do it again and this time cache should be False ###

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/document/admin/administrator/pages'),\
            method="GET",
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        data = json.loads(response.body)

        assert_equals(data['cache'], False)
        assert_equals(data['resp'], originalData['resp'])


    
        


        






