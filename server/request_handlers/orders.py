import json

import tornado.web
import tornado.gen
import tornado.httpclient

import stripe

import document

stripe.api_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

def post_to_stripe(order_data):
    '''
    Takes order data dict, extracts necessary data, and passes it to stripe 
    for processing.
    '''
    token = order_data['token']
    sub_total = int(order_data['subtotal'])
    tax = int(order_data['tax'])
    total = sub_total + tax
    charge = stripe.Charge.create(
         amount = total, # amt in cents
         currency = 'usd',
         card = token,
         description = 'samplepayment'
         )
    return charge

def check_payment(stripe_data, **kwargs):
    '''
    Takes a dictionary of stripe data and kwargs that represent keys in the 
    dictionary and the values that each key should have. Checks the dictionary 
    to see that each key yields the desired value. Returns true if so,
    false if not.
    '''
    for key in kwargs.keys():
        if kwargs[key] != stripe_data[key]:
            print stripe_date[key]
            return False
    return True

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
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/submitted".split('/')\
            )

            order['time'] = time.strftime("%m/%d/%Y %I:%M:%S")

            orders.append(order)

            resp = yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/submitted".split('/'),\
                data=orders\
                )

            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders-submitted",method='POST', headers=None, body="")

            raise tornado.gen.Return(True)


        @tornado.gen.coroutine
        def started(order):

            submitted = yield self.get_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/submitted".split('/')\
            )

            submitted = [ x for x in submitted if x['token'] != order['token'] ]

            yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/submitted".split('/'),\
                data=submitted\
                )

            started = yield self.get_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/started".split('/')\
            )

            started.append(order)

            yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/started".split('/'),\
                data=started\
                )

            yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders-submitted",method='POST', headers=None, body="")
            
            yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders-started",method='POST', headers=None, body="")
                
            raise tornado.gen.Return(True)


        @tornado.gen.coroutine
        def finished(order):
            
            started = yield self.get_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/started".split('/')\
            )

            started = [ x for x in started if x['token'] != order['token'] ]

            resp = yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/started".split('/'),\
                data=started\
                )

            finished = yield self.get_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/finished".split('/')\
            )

          
            try:
                
                processed = post_to_stripe(order)

                if check_payment(processed, paid=True, \
                        refunded=False, disputed=False):
                    finished.append(order)
            except Exception as e:
                print 'STRIPE ERROR:'
                print e
                print

            
            finished.append(order)

            resp = yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/finished".split('/'),\
                data=finished\
                )

            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders-started",method='POST', headers=None, body="")
            
            resp = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost/api/comet/orders-finished",method='POST', headers=None, body="")

            raise tornado.gen.Return(True)


        @tornado.gen.coroutine
        def cancel(order):


            orders = yield self.get_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path="orders/submitted".split('/')\
            )

            orders = [ x for x in orders if x['token'] != order['token'] ]

            yield self.save_data(\
                url="http://localhost:5984/"+param.split('/')[0]+"/administrator",\
                path=("orders/"+param.split('/')[2]).split('/'),\
                data=orders\
                )

           
            raise tornado.gen.Return(True)


        d = {'submitted': submitted,
             'started': started,
             'finished': finished,
             'cancel': cancel 
            }

        order = json.loads(self.request.body)

        yield d[param.split('/')[1]](order)

        self.finish()
        
