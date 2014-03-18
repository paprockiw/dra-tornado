import json

import tornado.web

import tornado.gen

import tornado.httpclient

import xmltodict

import pdb


class RequestHandler(tornado.web.RequestHandler):


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, param):
        """ 
        Gets document based on path. 
        """

        
        # database 
        database = param.split('/')[0]

        # document _id
        _id = param.split('/')[1]


        # get the document then extract prop
        pages = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=["pages"]\
            )

        sitemap = {
            'urlset': { 
                '@xmlns':"http://www.sitemaps.org/schemas/sitemap/0.9",
                'url':[
                
                ]
            }
        }

        def get_locs_to_sitemap(sitemap, pages, path='/', locs=[] ):
        
            for page in pages:
                locs.append({ 'loc': self.request.headers.get('Origin') + "/#!" + path + page['title'].lower().replace(" ", "-") })
                if len(page['subpages']) > 0:
                    get_locs_to_sitemap(sitemap, page['subpages'], path + page['title'].lower().replace(" ", "-") + '/', locs)

            return locs


        locs = get_locs_to_sitemap(sitemap, pages['pages'])

        sitemap['urlset']['url'] = sitemap['urlset']['url'] + locs


        fo = open("apps/root/sitemap.xml", "wb")
        fo.write( xmltodict.unparse(sitemap, pretty=True) )
        fo.close()

        self.finish()



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


    

    

    



    




