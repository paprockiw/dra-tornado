"""
module for setting up & clearing couchdb databases
"""

import couchdb
import couchdb.design
import os
import sys
import copy

from apps import apps

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
    print 'CREATE DB'
    if 'database' in app:
        print 'database in app', app['database']

    if 'database' not in app:
        print 'no db in app'
        return

    server = couchdb.Server()

    if app['database']['name'] not in server:
        print 'not in server'

        db = server.create(app['database']['name'])
        
        for key in app['database']:

            if key != 'name':

                db.save(app['database'][key])
    else: print 'IN SERVER'
            
                


def setup(id):
    """
    setup the couchdb databases
    """

    if id == 'all':

        for app in apps:

            if apps[app].get('database'):

                create_database(apps[app])

    else:

        create_database(apps[id])

   
