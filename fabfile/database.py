"""
module for setting up & clearing couchdb databases
"""

import couchdb
import couchdb.design
import os
import sys
import copy
# **apps**: all the apps to our project
from apps.apps import apps

# get the root path 
path = os.path.realpath(os.path.realpath(__file__) + '/../')
sys.path.append(path)

def clear(app):
    """
    Clears the database associated with the specified app. To clear all 
    applications, pass in the string 'all'.
    """
    # clear all the databases for every app
    if app == 'all':
        for key in apps:
            # if app has a database
            if apps[key].get('database'):
                server = couchdb.Server()
                # if database is in server
                if apps[key]['database']['name'] in server:
                    print 'remove database '+str(apps[key]['database']['name'])
                    # then delete database from server
                    del server[apps[key]['database']['name']]

    # else just delete the database for a specific app
    else:
        # if app has a database
        if apps[app].get('database'):
            server = couchdb.Server()
            # if database is in server
            if apps[app]['database']['name'] in server:
                print 'remove database '+str(apps[app]['database']['name'])
                # then delete database from server
                del server[apps[app]['database']['name']]


def clearup_schemas_and_collections(doc):
    """
    Takes an argument that is the name of a document, and then clears all
    schemas and collections for that document.
    """
    # for each key in document
    for key in doc:
        # if property is a dictionary
        if type(doc[key]) == dict:
            # if property is a schema
            if doc[key].get('schema'):
                # get the schema
                schema = doc[key].get('schema')
                obj = {}
                # for each field in schema
                for field in schema:
                    obj[field.keys()[0]] = field[field.keys()[0]]
                # do a recursive call to extact schemas and collections
                doc[key] = clearup_schemas_and_collections(obj)
            # if property is a collction
            elif doc[key].get('collection'):
                # then just set is as an empty list
                doc[key] = []
            # if property has a default value setup
            elif doc[key].get('value'):
                # then assign default value
                doc[key] = doc[key].get('value')
            elif doc[key].get('map-template'):
                # then assign default value
                doc[key] = content.templates[doc[key].get('map-template')]
            # if property is a dictionary 
            elif type(doc[key]) == dict:
                # then see if there are more schemas and colloctions to clear up
                doc[key] = clearup_schemas_and_collections(doc[key])

        # if property is a list
        elif type(doc[key]) == list:
            # check to see if there are more schemas and collections to clearup
            for item in doc[key]:
                clearup_schemas_and_collections(item)

    return doc


def create_database(app):
    """
    Takes the name of an app and creates a database for it.
    """
    server = couchdb.Server()
    # if database is not in server
    if app['database']['name'] not in server:
        print "create database for "+str(app['database']['name'])
        db = server.create(app['database']['name'])
        # create documents and design/document for database 
        for _id in app['database']:
            if type(app['database'][_id]) == dict:
                # if _id is of type document then create a document based on schema
                if app['database'][_id].get('document'):
                    # do a deep copy of document so that we don't overide 
                    #the blueprint when we clear if of schemas and collections
                    doc = copy.deepcopy(app['database'][_id]['document'])
                    # assign _id to document
                    doc['_id'] = _id
                    # clear up all schemas and collection specifications for document
                    clearup_schemas_and_collections(doc)
                    # save document to couchdb
                    db.save(doc)
                # elif _id is a design document then create a _design/ document
                elif '_design' in _id:
                    v_dict = app['database'][_id]['views']
                    for v_name in v_dict:
                        view = couchdb.design.\
                        ViewDefinition(_id, 
                                       v_name, 
                                       v_dict[v_name]['map'], 
                                       reduce_fun=v_dict[v_name]['reduce'], 
                                       # reduce default is None, which the 
                                       # ViewDefinition object can handle
                                       language='python')
                        view.sync(db)


def setup(app):
    """
    setup the couchdb databases
    """
    # create all the databases for every app
    if app == 'all':
        for key in apps:
            # if app has a database
            if apps[key].get('database'):
                create_database(apps[key])
    # else just create database for specific app
    else:
        # create database for specific app
        if apps[app].get('database'):
            create_database(apps[app])
