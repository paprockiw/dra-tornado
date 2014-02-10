import document

class Order(document.RequestHandler):

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, param):
        # get the document then extract prop
        data = yield self.get_data(\
            url="http://localhost:5984/rpm_menu/administrator",\
            path="orders/"+param\
            )
        self.finish(data)
        print data


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, param):
        def submitted(self, data):
            print data

        def started(self, data):
            print data

        def finished(self, data):
            print data

        d = {'submitted': self.submitted,
             'started': self.started,
             'finished': self.finished 
            }

        data = json.loads(self.request.body)
        d[param](data)
        
