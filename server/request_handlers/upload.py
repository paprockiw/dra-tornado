import json
import shutil
import os
import sys

import tornado.web
import tornado.gen
import tornado.httpclient

from PIL import Image

from config import config

import pdb


class RequestHandler(tornado.web.RequestHandler):
    """
    request handler for upload
    """


    @tornado.web.asynchronous
    def get(self, path): 
        """ 
        get all upload images
        """        

        # setup a config file
        files = os.listdir(config['upload']+"/"+path)

        # filter out files
        filesFilter = [file for file in files if file != '.DS_Store']

        response = {
            "resp": filesFilter
        }


        self.finish(response)



    @tornado.web.asynchronous
    def post(self, path):
        """ 
        move latest uploaded file path and create 4 new images
        """


        ### move latest uploaded image ###

        file_path = self.get_argument('file.path')

        file_name = self.get_argument('file.name').replace(" ", "-").lower() 
  
        if not os.path.exists(config['upload']+"/"+path):
            os.makedirs(config['upload']+"/"+path)
        
        shutil.move( file_path, config['upload']+"/"+path+"/"+file_name )


        ### create 6 new images ###


        sizes = {
            "thum": (180, 180),
            "phone": (480,480),
            "phone_highres": (976,976),
            "tablet": (768,768),
            "tablet_highres": (1536,1536),
        }


        for key in sizes:

            try:
                im =  Image.open(config['upload']+"/"+path+"/"+file_name)
            except:
                print "Unable to load image"


            if not os.path.exists(config['upload']+"/"+path+"/"+key):
                os.makedirs(config['upload']+"/"+path+"/"+key)

            
            im.thumbnail(sizes[key], Image.ANTIALIAS)
            im.save(config['upload']+"/"+path+"/"+key+"/"+file_name)

        
        self.finish()


    

    



    



    




