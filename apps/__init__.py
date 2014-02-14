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
                        "started": [],
                        "finished": []
                    }
                }
            }
        },

        # request_hander is the only key right now in each sub-dict.
        # consider moving these to format like /login/(.+) : <REQUEST_HANDLER>
        "routes": {
            "/login/(.+)":{ 
                'request_handler': 'server.request_handlers.login'
            },
            "/document/(.+)":{ 
                'request_handler': 'server.request_handlers.document'
            },
            "/orders/(.+)": {
                'request_handler': 'server.request_handlers.orders'
            },
            "/comet/(.+)": {
                'request_handler': 'server.request_handlers.comet'
            }
        }
    },

    "menu": {

        "repo":"https://github.com/ruahman/rpm-menu.git",

        "branch": "master"

    }

}

