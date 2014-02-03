apps =  {
    'admin': {
        "database": {
            "name": "menu",
            "administrator": {
                "orders": {
                    "submitted":[],
                    "accepted": [],
                    "finished": []
                }
            },
        },
        "routes": {
            "/login":{ 'request_handler': 'MainHandler'
            },
            "/orders":{ 'request_handler': 'MainHandler'
            }
        }
    },
    "menu": {
        "routes": {
            "/pages": {
            },
            "/data": {
            }
        }
    }
}

