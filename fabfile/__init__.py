"""
runs fab commands for building and deploying projects
"""

import os
import sys

from fabric.api import task, env, local, lcd

from database import setup_database, clear_database
from server import run_server
from apps import apps

# add to path so that we can import apps
path = os.path.realpath(os.path.realpath(__file__) + '/../')
sys.path.append(path)

env.hosts = ['localhost']


def init(app='all'):
    """
    initialize the databases and repositories for our apps
    """
    
    if app == 'all':
        for key in apps:

            if 'database' in apps[key]:
                init_database(key)

            if 'repo' in apps[key]:
                init_repo(key,apps[key]['repo'],apps[key]['branch'])

    else:
        if 'database' in apps[app]:
            setup_database(app)
        if 'repo' in apps[app]:
            init_repo(app,apps[app]['repo'],apps[app]['branch'])


def init_database(app):
    """
    initializes the database
    """

    setup_database(apps[app]['database'])


def init_repo(app,repo,branch):
    """
    clones repo for app and sets the branch
    """

    with lcd("apps"):
        local("rm -rf "+app)
        local("git clone "+repo+" "+app)
        with lcd(app):
            local("git checkout "+branch)


def clear():
    """
    clear database and repo for our apps
    """

    for key in apps:
        if 'database' in apps[key]:
            clear_database(apps[key]['database'])
        
        if 'repo' in apps[key]:
            with lcd("apps"):
                local("rm -rf "+key)

    
def server():
    """
    run our tornado app
    """

    run_server(apps)

