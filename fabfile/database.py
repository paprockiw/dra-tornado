"""
module for setting up & clearing couchdb databases
"""

import couchdb
import couchdb.design
import os
import sys
import copy


def setup_database(database):
    """
    setup couchdb database
    """

    dbName = database.keys()[0]

    server = couchdb.Server()

    if dbName not in server:

        db = server.create(dbName)

        pdb = __import__('pdb')
        pdb.set_trace()

        documents = database[database.keys()[0]]


        for doc in documents:
            db[doc] = documents[doc]


def clear_database(name, database):
    """
    clear database from couchdb
    """

    server = couchdb.Server()

    if name in server:

        del server[name]


def view_function(path, f_type='map'):
    """
    Decorator function for adding a view function to a design document. 
    Specify path to view in couchdb, then specify the function type (map/reduce). 
    Can be used up to 2 times for a given path, once for map, once for reduce.
    """
    assert f_type in ('map', 'reduce'), \
        "f_type argument in view_function must be either 'map' or 'reduce'"

    path_array = path.split('/')
    v_name = path_array[-1] # view name
    path_to_doc = "/".join(path_array[:2])

    database.setdefault(path_to_doc,
            {"_id": string.join(path_to_doc,'/'),
            "language":"python",
            "views" : {v_name:{'map':None, 
                               'reduce':None}
                      }
            }
    )

    def decorator(func):
        '''
        Assigns the function to the specified path. This closure makes it 
        possible for different functions to have the same name if they are in 
        different views.
        '''
        database[path_to_doc]['views'][v_name][f_type] = func
        return func

    return decorator






   
