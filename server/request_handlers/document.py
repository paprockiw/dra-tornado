"""
Setup Request handler for Documents 
"""

## system imports ##

import json
import urllib
import redis

import pdb


## third party imports ##

import tornado.web
import tornado.gen
import tornado.httpclient


# setup redis

redisServer = redis.Redis("localhost")


class RequestHandler(tornado.web.RequestHandler):
    """
    request handler for retriving and saving data 
    to any arbitrary document in a database based on path
    """


    @tornado.gen.coroutine # so function can use coroutines
    @tornado.web.asynchronous # so function can be called asynchronously
    def get(self, param): 
        """ 
        get data from document base on path. 
        """


        ### get the data ###

        # database 
        database = param.split('/')[0]

        # document _id
        _id = param.split('/')[1]

        # path to data in document  
        path = param.split('/')[2:]

        # get data from document
        data, cached = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path\
            )


        ### return data ###

        
        self.finish({
            "resp": data,
            "cached": cached
            })
       


    @tornado.gen.coroutine # so function can use coroutines
    @tornado.web.asynchronous # so function can be called asynchronously
    def post(self, param):
        """ 
        post data to document based on path. 
        """
        
        # database 
        database = param.split('/')[0]

        # _id of document
        _id = param.split('/')[1]

        # path to data in document
        path = param.split('/')[2:]

        
        # data for updating the document
        data = json.loads(self.request.body)
        
        # save data to document based on path
        resp = yield self.save_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path,\
            data=data\
            )

        self.finish(resp)


    def _handle_request_exception(self, e):
        """
        exception handler for request handler
        """

        self.set_status(400)
        self.finish("tornado threw an exception")


    def custom_error_response(self, response):
        """
        sends a custom error response to user.
        """

        self.set_status(400)
        self.finish(response)


    @tornado.gen.coroutine # allow function to use generators
    def get_data(self,url,path):
        """
        get data from document based on path
        """

        ### get data ###

        # pdb.set_trace()

        data = redisServer.get(url+"/"+"/".join(path))
        
        if data != None:
            print "cached"
            data = json.loads(data)

            raise tornado.gen.Return((data,True))

        else:
            print "couchdb"
            # get the document
            doc = yield self.get_doc(url)

            # get data from property
            data = yield self.get_prop(\
                doc=doc,\
                path=path\
                )

            # pdb.set_trace()

            redisServer.set(url+"/"+"/".join(path), json.dumps(data))

            raise tornado.gen.Return((data,False))



        ### return data ###

        



    @tornado.gen.coroutine # allow function to use generators 
    def get_doc(self, url):
        """
        fetches and returns couchdb doc
        """

        ### get document ### 

        resp = yield tornado.httpclient.AsyncHTTPClient().fetch(url)

        # convert it to dict
        doc = json.loads(resp.body)


        ### return document ###

        raise tornado.gen.Return(doc)


    @tornado.gen.coroutine # allow function to use generators 
    def get_prop(self,doc,path):
        """
        extract data from doc using path
        """

        ### get data from prop using path ###

        prop = doc
        for key in path:
            if key.isdigit():
                prop = prop[int(key)]
            else:
                prop = prop[key]

        ### return property ###

        raise tornado.gen.Return(prop)


    @tornado.gen.coroutine # allow function to use generators 
    def save_data(self,url,path,data):
        """
        save data to document
        """

        # get doc
        doc = yield self.get_doc(\
            url=url,\
            )

        # set doc property
        doc = self.set_prop(\
            doc=doc,\
            path=path,\
            data=data\
            )

        # save doc
        resp = yield self.save_doc(\
            url=url,\
            doc=doc,\
            )

        # clear it from redis
        redisServer.delete(url+"/"+"/".join(path))

        # return responce
        raise tornado.gen.Return(resp)


    def set_prop(self,doc,path,data):
        """
        set document acording to path and data
        """

        if len(path) > 0:
            key = path[0]

            if type(doc) == list:
                key = int(key)
            
            if len(path) > 1:
                doc[key] = self.set_prop(\
                    doc=doc[key],\
                    path=path[1:],\
                    data=data\
                    )
            else:
                doc[key] = data

        else:

            for key in data:
                doc[key] = data[key]

        return doc


    @tornado.gen.coroutine 
    def save_doc(self,url,doc):
        """
        save couchdb document
        """

        request = tornado.httpclient.HTTPRequest(\
            url=url,\
            method="PUT",\
            headers={'Content-Type': 'application/json; charset=UTF-8'},\
            body=json.dumps(doc)\
            )

        resp = yield tornado.httpclient.AsyncHTTPClient().fetch(request)

        raise tornado.gen.Return(resp.body)



    




