"""
dictionary that we user for setting up our apps
"""

apps =  {

    "admin": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "admin",

        "database": {
            "admin": { 
                "administrator": {
                    "users": {
                        "administrator":"admin",
                        "password":"swipe",
                        "users":[]
                    },
                    "data": {
                        "menu":{
                            "categories":[]
                        },
                        "blog":{
                            "categories":[]
                        },
                        "comicbooks":{
                            "publishers":[]
                        }
                    },
                    "orders": {
                        "submitted":[],
                        "started": [],
                        "finished": []
                    },
                    "pages":{
                        "pages":[]
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
            "/upload/(.+)": {
                'request_handler': 'server.request_handlers.upload'
            },
            "/comet/(.+)": {
                'request_handler': 'server.request_handlers.comet'
            },
            "/seo/(.+)": {
                'request_handler': 'server.request_handlers.seo'
            }
        }
    },


    "menu-admin": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "menu-admin",

        "database": {
            "menu-admin": { 
                "administrator": {
                    "users": {
                        "administrator":"admin",
                        "password":"swipe",
                        "users":[]
                    },
                    "data": {
                        "menu":{
                            "categories":[]
                        },
                        "blog":{
                            "categories":[]
                        },
                        "comicbooks":{
                            "publishers":[]
                        }
                    },
                    "orders": {
                        "submitted":[],
                        "started": [],
                        "finished": []
                    },
                    "pages":{
                        "pages":[]
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
            "/upload/(.+)": {
                'request_handler': 'server.request_handlers.upload'
            },
            "/comet/(.+)": {
                'request_handler': 'server.request_handlers.comet'
            }
        }
    },

    "comic-admin": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "comic-admin",

        "database": {
            "comic-admin": { 
                "administrator": {
                    "users": {
                        "administrator":"admin",
                        "password":"swipe",
                        "users":[]
                    },
                    "data": {
                        "menu":{
                            "categories":[]
                        },
                        "blog":{
                            "categories":[]
                        },
                        "comicbooks":{
                            "publishers":[]
                        }
                    },
                    "orders": {
                        "submitted":[],
                        "started": [],
                        "finished": []
                    },
                    "pages":{
                        "pages":[]
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
            "/upload/(.+)": {
                'request_handler': 'server.request_handlers.upload'
            },
            "/comet/(.+)": {
                'request_handler': 'server.request_handlers.comet'
            }
        }
    },

    "root": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "master"

    },

    "menu": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "menu"

    },


    "comic": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "comic"

    }

}

