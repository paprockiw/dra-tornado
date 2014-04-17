"""
dictionary that we user for setting up our apps
"""

apps =  {

    "admin": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "admin",

        "databaseName": "admin",

        "databaseSchema": {
            "administrator": {
                "users": {
                    "administrator":"admin",
                    "password":"swipe"
                },
                "data": {
                    "blog":{
                        "categories":[]
                    },
                },
                "payment": {
                    "orders":[]
                },
                "pages":{
                    "pages":[]
                }
            }  
        },

        # request_hander is the only key right now in each sub-dict.
        # consider moving these to format like /login/(.+) : <REQUEST_HANDLER>
        "routes": {
            "/login/(.+)":{ 
                'requestHandler': 'server.request_handlers.login'
            },
            "/document-secure/(.+)":{ 
                'requestHandler': 'server.request_handlers.document_secure'
            },
            "/pages/(.+)":{ 
                'requestHandler': 'server.request_handlers.pages'
            },
            "/orders/(.+)": {
                'requestHandler': 'server.request_handlers.orders'
            },
            "/upload/(.+)": {
                'requestHandler': 'server.request_handlers.upload'
            },
            "/comet/(.+)": {
                'requestHandler': 'server.request_handlers.comet'
            },
            "/seo/(.+)": {
                'requestHandler': 'server.request_handlers.seo'
            }
        }
    },

    "swipe": {

        "repo":"https://github.com/ruahman/rpm-angular-react.git",

        "branch": "master"

    }

}

