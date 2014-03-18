import json

import urllib

import tornado.web

import tornado.gen

import tornado.httpclient

import pdb


class RequestHandler(tornado.web.RequestHandler):


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, param): 
        """ 
        Gets document. 
        """

        # database 
        database = param.split('/')[0]

        # document _id
        _id = param.split('/')[1]

        # property of document
        path = param.split('/')[2:]

        # get the document then extract prop
        data = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path\
            )

        if type(data) == list:
            self.finish({
                "list": data
                })
        else:
            self.finish(data)


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, param):
        """ 
        Gets document based on path. 
        """
        
        # database 
        database = param.split('/')[0]

        # _id of document
        _id = param.split('/')[1]

        # path to property of document
        path = param.split('/')[2:]

        
        # data for updating the document
        # data = json.loads(self.get_argument('data'))
        data = json.loads(self.request.body)
        
        # save doc based on data
        resp = yield self.save_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path,\
            data=data\
            )

        # # setup sitemap
        # post_data = {}
        # body = urllib.urlencode(post_data)

        # seo = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/seo/"+database,method='POST', headers=None, body=body)

        # print seo

        
        self.finish(resp)


    def return_error(self,response):
        """
        Returns error response to user.
        """

        self.set_status(400)
        self.finish(response)


    @tornado.gen.coroutine 
    def get_data(self,url,path):
        """
        get document then return property specified from path
        """
        

        doc = yield self.get_doc(url)



        data = yield self.get_prop(\
            doc=doc,\
            path=path\
            )



        raise tornado.gen.Return(data)



    @tornado.gen.coroutine 
    def get_doc(self, url):
        """
        fetches and returns couchdb doc
        """

        resp = yield tornado.httpclient.AsyncHTTPClient().fetch(url)
        doc = json.loads(resp.body)
        raise tornado.gen.Return(doc)


    @tornado.gen.coroutine 
    def get_prop(self,doc,path):
        """
        extract data from doc using path
        """


        prop = doc
        for key in path:
            if key.isdigit():
                prop = prop[int(key)]
            else:
                prop = prop[key]

        raise tornado.gen.Return(prop)


    @tornado.gen.coroutine 
    def save_data(self,url,path,data):
        """
        save data to document
        """

        # get doc
        doc = yield self.get_doc(\
            url=url,\
            )

        # set doc
        doc = self.set_doc(\
            doc=doc,\
            path=path,\
            data=data\
            )

        # save doc
        resp = yield self.save_doc(\
            url=url,\
            doc=doc,\
            )

        # return responce
        raise tornado.gen.Return(resp)


    def set_doc(self,doc,path,data):
        """
        set document acording to path and data
        """

        if len(path) > 0:
            key = path[0]

            if type(doc) == list:
                key = int(key)
            
            if len(path) > 1:
                doc[key] = self.set_doc(\
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



    




