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


def init():
    """
    initialize the databases and repositories for our apps
    """
    
    for key in apps:

        if 'database' in apps[key]:
            setup_database(apps[key]['database'])

        if 'repo' in apps[key]:
            with lcd("apps"):
                local("rm -rf "+key)
                local("git clone "+apps[key]['repo']+" "+key)


def clear():
    """
    clear database and repo for our apps
    """

    for key in apps:
        if 'database' in apps[key]:
            clear_database(apps[key]['database'])
            local("rm -rf "+apps[key]['repo'])

    
def server():
    """
    run our tornado app
    """

    run_server(apps)

