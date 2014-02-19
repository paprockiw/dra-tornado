import stripe

# OLD VERSION:
#class Stripe(tornado.web.RequestHandler):
#    def post(self):
#        token = self.get_argument('stripeToken')
#        #self.write(token)
#        # Store key in separate config?
#        stripe.api_key = 'zGG4QHGhMlBElVBCioobCucrHJdaoeFP'
#        charge = stripe.Charge.create(
#				 amount = 1000, # amt in cents
#				 currency = 'usd',
#				 card = token,
#				 description = 'samplepayment'
#		)
#        print charge
#        self.write('payment accepted')


stripe.api_key = 'zGG4QHGhMlBElVBCioobCucrHJdaoeFP'

def post_to_stripe(order_data):
    '''
    Takes order data dict, extracts necessary data, and passes it to stripe 
    for processing.
    '''
    token = order_data['token']
    sub_total = order_data['subtotal']
    tax = order_data['tax']
    total = int((sub_total + tax) * 1000)
    charge = stripe.Charge.create(
   		 amount = total, # amt in cents
   		 currency = 'usd',
   		 card = token,
   		 description = 'samplepayment'
         )
    return charge

