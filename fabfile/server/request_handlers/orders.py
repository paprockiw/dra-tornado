import json

import tornado.web
import tornado.gen
import tornado.httpclient

import document

from stripe_handler import post_to_stripe, check_payment

#import pdb

class RequestHandler(document.RequestHandler):

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, param):
        

        orders = yield self.get_data(\
            url="http://localhost:5984/rpm-menu/administrator",\
            path=("orders/"+param).split('/')\
            )

        if type(orders) == list:
            self.finish({
                "list": orders
                })
        else:
            self.finish(orders)
        


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, param):


        @tornado.gen.coroutine
        def submitted(order):

            import time

            orders = yield self.get_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/submitted".split('/')\
            )

            order['datatime'] = time.strftime("%m/%d/%Y %I:%M:%S")

            orders.append(order)

            resp = yield self.save_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/submitted".split('/'),\
                data=orders\
                )

            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders/submitted",method='POST', headers=None, body="")

            raise tornado.gen.Return(True)


        @tornado.gen.coroutine
        def started(order):
            print order

            submitted = yield self.get_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/submitted".split('/')\
            )

            submitted = [ x for x in submitted if x['datatime'] != order['datatime'] ]

            resp = yield self.save_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/submitted".split('/'),\
                data=submitted\
                )

            started = yield self.get_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/started".split('/')\
            )

            started.append(order)

            resp = yield self.save_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/started".split('/'),\
                data=started\
                )

            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders/submitted",method='POST', headers=None, body="")
            
            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders/started",method='POST', headers=None, body="")
                
            raise tornado.gen.Return(True)


        @tornado.gen.coroutine
        def finished(order):
            print order 
            started = yield self.get_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/started".split('/')\
            )

            started = [ x for x in started if x['datatime'] != order['datatime'] ]

            resp = yield self.save_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/started".split('/'),\
                data=started\
                )

            finished = yield self.get_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/finished".split('/')\
            )

            # somewhere here process stripe
#            print '-'*50
#            print 'SRIPE ORDER INFO:'
            try:
                processed = post_to_stripe(order)
#                print processed
                if check_payment(processed, paid=True, \
                        refunded=False, disputed=False):
                    finished.append(order)
            except Exception as e:
                print 'STRIPE ERROR:'
                print e
                print
            

            resp = yield self.save_data(\
                url="http://localhost:5984/rpm-menu/administrator",\
                path="orders/finished".split('/'),\
                data=finished\
                )

            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders/started",method='POST', headers=None, body="")
            
            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders/finished",method='POST', headers=None, body="")

            raise tornado.gen.Return(True)




        d = {'submitted': submitted,
             'started': started,
             'finished': finished 
            }

        order = json.loads(self.request.body)

        yield d[param](order)

        self.finish()
        
