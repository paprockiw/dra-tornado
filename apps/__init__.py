"""
dictionary that we user for setting up our apps
"""

apps =  {

    "menu-admin": {

        "repo":"https://github.com/ruahman/rpm-menu-admin.git",

        "branch": "master",

        "database": {
            "rpm-menu": { 
                "administrator": {
                    "users": {
                        "administrator":"admin",
                        "password":"swipe",
                        "users":[]
                    },
                    "orders": {
                        "submitted":[],
                        "accepted": [],
                        "finished": []
                    }
                }
            }
        },

        "routes": {
            #"login/(.+)"
            "/login/(.+)":{ 
                'request_handler': 'server.request_handlers.login'
            },
            "/document/(.+)":{ 
                'request_handler': 'server.request_handlers.document'
            }
        }
    },

    "menu": {

        "repo":"https://github.com/ruahman/rpm-menu.git",

        "branch": "master"

    }

}

