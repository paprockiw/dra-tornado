"""
runs fab commands for building and deploying projects
"""
from fabric.api import task
from fabric.api import env

import database

from server import runserver
#from apps.apps import apps

env.hosts = ['localhost']

def init(app='all'):
    """
    Takes the name of an app as an argument and sets up a database for it 
    based on the specified schema. With no arguments, it sets up all apps in 
    apps directory.
    """
    # setup database
    database.setup(app)
