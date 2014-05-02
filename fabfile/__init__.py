"""
fab commands for building and deploying our project
"""

## system imports ##
import os
import sys
# import pdb

## third party imports ##
from fabric.api import task, env, local, lcd

## project modules ##
import database # handle database actions
import apps # handles configuration of our apps
from server import run # handles running tornado server



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
            if 'database' in apps.apps[key]:
                # init database
                database.init(key)

           
            # create app from repo and branch
            init_app(app=key, repo=apps.apps[key]['repo'], branch=apps.apps[key]['branch'])


    ## init a single app ##
    else:

        # get database of app
        if 'database' in apps.apps[app]:
            database.init(app)

        # create app from repo and branch
        init_app(app=app, repo=apps.apps[app]['repo'], branch=apps.apps[app]['branch'])



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
            if 'database' in apps.apps[key]:

                # clear database
                database.clear(key)
            
            # remove app from project
            remove_app(key)


    ## clear a single app ##
    else:

        # clear database
        if 'databaseName' in apps.apps[app]:
            database.clear(app)

        # remove app from project
        remove_app(app)

    
def server():
    """
    run server
    """

    run()


