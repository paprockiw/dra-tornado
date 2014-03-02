import json

import shutil

import os

import tornado.web

import tornado.gen

import tornado.httpclient

from PIL import Image

import pdb


class RequestHandler(tornado.web.RequestHandler):


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, path): 
        """ 
        get all upload images
        """

        files = os.listdir("/Users/ruahman/swipe-tech-apps/rpm-tornado/apps/"+path)

        filesFilter = [file for file in files if file != '.DS_Store']

        print files

        response = {
            "files": filesFilter
        }


        self.finish(response)


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, path):
        """ 
        post to upload
        """

        file_path = self.get_argument('file.path')

        file_name = self.get_argument('file.name') 
        
        shutil.move( file_path, "/Users/ruahman/swipe-tech-apps/rpm-tornado/apps/"+path+"/"+file_name )

        size = (280, 280)

        try:
            im =  Image.open("/Users/ruahman/swipe-tech-apps/rpm-tornado/apps/"+path+"/"+file_name)
        except:
            print "Unable to load image"

        im.thumbnail(size, Image.ANTIALIAS)

        im.save("/Users/ruahman/swipe-tech-apps/rpm-tornado/apps/"+path+"/thum-"+file_name)
        
        self.finish({})


    

    



    



    




