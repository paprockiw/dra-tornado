"""
dictionary that we user for setting up our apps
"""

apps =  {

    "admin": {

        # "repo":"https://github.com/ruahman/rpm-menu.git",

        "database": {
            "name": "rpm-menu",
            "administrator": {
                "orders": {
                    "submitted":[],
                    "accepted": [],
                    "finished": []
                }
            },
        },

        "routes": {
            "/login":{ 
                'request_handler': 'LoginHandler'
            },
            "/orders":{ 
                'request_handler': 'DocumentHandler'
            }
        }
    },

    "menu": {

        "repo":"https://github.com/ruahman/rpm-menu.git"

    }
}

