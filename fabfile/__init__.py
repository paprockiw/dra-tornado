"""
fab commands for building and deploying projects
"""

import os
import sys

from fabric.api import task, env, local, lcd

import database
import apps
from server import run


import pdb

env.hosts = ['localhost']


def init(app='all'):
    """
    initialize the databases and apps for our project
    """

    def init_repo(app, repo, branch):
        """
        init repository
        """

        with lcd("apps"):
            local("rm -rf "+app)
            local("git clone "+repo+" "+app)
            with lcd(app):
                local("git checkout "+branch)
    
    if app == 'all':

        for key in apps.apps:

            if 'databaseName' in apps.apps[key]:
                database.init(key)

            if 'repo' in apps.apps[key]:
                init_repo(key,apps.apps[key]['repo'],apps.apps[key]['branch'])

    else:

        if 'databaseName' in apps.apps[app]:
            database.init(app)

        if 'repo' in apps.apps[app]:
            init_repo(app, apps.apps[app]['repo'], apps.apps[app]['branch'])


def clear(app='all'):
    """
    clear database and repo for our apps
    """

    def remove_repo(repo):
        """
        remove repository
        """

        with lcd("apps"):
            local("rm -rf "+repo)

    if app == 'all':

        for key in apps.apps:
            if 'databaseName' in apps.apps[key]:
                database.clear(apps.apps[key]['databaseName'])
            
            if 'repo' in apps.apps[key]:
                remove_repo(key)

    else:
        database.clear(apps.apps[app]['databaseName'])

        if 'repo' in apps.apps[app]:
            remove_repo(app)

    
def server():
    """
    run server
    """

    run()


