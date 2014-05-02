"""
fab commands for building and deploying our project
"""

import os
import sys

from fabric.api import task, env, local, lcd

import database
import apps
from server import run

# import pdb

env.hosts = ['localhost']


def init(app='all'):
    """
    initialize the databases and apps for our project
    """

    def init_app(app, repo, branch):
        """
        init app
        """

        # go to apps
        with lcd("apps"):

            # remove app
            local("rm -rf "+app)

            # clone repo
            local("git clone "+repo+" "+app)

            # go to branch
            with lcd(app):
                local("git checkout "+branch)

    
    ## init all apps in project ##
    if app == 'all':

        # loop through all the apps
        for key in apps.apps:

            # if app has a database
            if 'databaseName' in apps.apps[key]:
                # init database
                database.init(key)

           
            # create app from repo and branch
            init_app(key,apps.apps[key]['repo'],apps.apps[key]['branch'])


    ## init a single app ##
    else:

        # get database of app
        if 'databaseName' in apps.apps[app]:
            database.init(app)

        # create app from repo and branch
        init_app(app, apps.apps[app]['repo'], apps.apps[app]['branch'])


def clear(app='all'):
    """
    clear database and apps from our project
    """

    def remove_app(repo):
        """
        remove app from project
        """

        with lcd("apps"):
            local("rm -rf "+repo)


    ## clear all apps from project ##
    if app == 'all':

        for key in apps.apps:

            # if app has a database
            if 'databaseName' in apps.apps[key]:

                # clear database
                database.clear(apps.apps[key]['databaseName'])
            
            # clear repo from project
            remove_app(key)


    ## clear a single app ##
    else:

        # clear database
        if 'databaseName' in apps.apps[app]:
            database.clear(apps.apps[app]['databaseName'])

        # clear repo from project
        remove_app(app)

    
def server():
    """
    run server
    """

    run()


