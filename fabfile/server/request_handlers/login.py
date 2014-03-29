"""
This is the request handler incharge of login in users
"""

import json

import tornado.web
import tornado.gen

import document

class RequestHandler(document.RequestHandler):

    @tornado.web.asynchronous # sets up route to be asynchronous
    @tornado.gen.coroutine # allows us to use generators and coroutins for async io
    def post(self, param):
        """
        user post login reqest. 
        passes in paramiters usernameOrEmail, and password.
        if everything checks out then it finishes connections.
        if anything wrong happens an exception is thrown
        """

        # extact database from path
        database = param.split('/')[0]

        # extract id of document
        _id = param.split('/')[1]

        # extact path to property of document 
        path = param.split('/')[2:]

        # get post data
        data = json.loads(self.request.body)

        # extract username from data
        username = data['username']

        # extract password from data
        password = data['password']

        # get users 
        users = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path\
            )

        # check is username is administrator
        if username == users['administrator']:

            # check if password is correct
            if users['password'] == password:

                # assign secrit cookie
                self.set_secure_cookie("login", 'true',  expires_days=None)

            else:

                self.return_error('incorect password')

        else:

            self.return_error('incorect username')


        self.finish()



