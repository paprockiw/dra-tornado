"""
module for setting up & clearing couchdb databases
"""

import couchdb
import couchdb.design
import os
import sys
import copy

from apps.apps import apps

# get the root path 
path = os.path.realpath(os.path.realpath(__file__) + '/../')
sys.path.append(path)

def clear(app):
    """
    Clears the database associated with the specified app. To clear all 
    applications, pass in the string 'all'.
    """
    
    for key in apps:
        
        if apps[key].get('database'):

            server = couchdb.Server()

            if apps[key]['database']['name'] in server:

                del server[apps[key]['database']['name']]

   


def create_database(app):
    """
    Takes the name of an app and creates a database for it.
    """

    server = couchdb.Server()

    if app['database']['name'] not in server:

        db = server.create(app['database']['name'])
        
        for key in app['database']:

            if key not name:

                db.save(app['database'][key])
            
                


def setup(id):
    """
    setup the couchdb databases
    """

    if id == 'all':

        for app in apps:

            if apps[key].get('database'):

                create_database(apps[key])

    else:

        create_database(apps[id])

   
