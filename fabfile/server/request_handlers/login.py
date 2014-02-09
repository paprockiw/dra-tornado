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

        # response we send back
        response = {
            'login':False
        }


        database = param.split('/')[0]

        print database

        # _id of document
        _id = param.split('/')[1]

        print _id

        # path to property 
        path = param.split('/')[2:]

        print path

        # get username
        # username = self.get_argument('username')

        data = json.loads(self.request.body)

        username = data['username']

        print username

        password = data['password']

        print password

        users = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path\
            )

        print users

        if username == users['administrator']:

            if users['password'] == password:

                self.set_secure_cookie("login", 'true',  expires_days=None)

                response['login'] = True

            else:

                self.return_error('incorect password')

        else:

            self.return_error('incorect username')


        self.finish(response)



