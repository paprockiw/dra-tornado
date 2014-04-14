import stripe

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
