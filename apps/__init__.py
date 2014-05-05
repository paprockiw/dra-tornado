"""
dictionary that we user for setting up our apps
"""

apps =  {

    # admin: admistrator app for our project
    "admin": {

        "repo":"https://github.com/ruahman/rpm-angular-polymer-react.git",

        "branch": "admin",

        # name of databse
        "database": "admin",

        # schema of documents in database
        "schema": {

            # administrator document
            "administrator": {

                # pages to our website
                "pages":{
                    "pages":[]
                },

                # data that pages refer to
                "data": {
                    "blog":{
                        "categories":[]
                    },
                },

                # admin info
                "users": {
                    "administrator":"admin",
                    "password":"swipe"
                }
   
            }  
        },

        # routes for our app
        "routes": {

            "/login/(.+)": "server.request_handlers.login",

            "/document-secure/(.+)": "server.request_handlers.document_secure",
            
            "/pages/(.+)": "server.request_handlers.pages"
               
        }
    },

    # swipe: client app for our project
    "swipe": {

        "repo":"https://github.com/ruahman/rpm-angular-polymer-react.git",

        "branch": "master"

    }

}

