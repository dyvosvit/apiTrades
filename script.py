#generate new API key/secret from Poloniex and put them here
#it worked for you, you use and like it = donate any amount you wish

#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

pkey = ''
spkey= ''

apidelay = 0.888

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import Request, urlopen, URLError, HTTPError
    from urllib import urlencode

import json, ssl
import time, datetime
from datetime import date, datetime
import calendar
import hmac,hashlib



def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                            
        return after

    def api_query(self, command, req={}):

        if(command == "returnTicker" or command == "return24Volume"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read())
        elif(command == "returnOrderBook"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif(command == "returnMarketTradeHistory"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        else:
            req['command'] = command
            req['nonce'] = int(time.time()*1000)
            #post_data = bytes(urlencode(req),'utf-8')
            post_data = urlencode(req)

            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }
            print(req)
            try:
                ret = urlopen(Request('https://poloniex.com/tradingApi', post_data, headers))
            except HTTPError as e:
                print("Polo is lagging, we've got "+str(e.code)+" error  ... continue")
                print(e.read())
                return ''
            except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
                return ''
            except ssl.SSLError:
                print("Internet is lagging, we've got SSL error")
                return ''
                
            jsonRet = json.loads(ret.read())

            return self.post_process(jsonRet)

    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})
        
    def returnOrderTrades(self, orderNumber):
    	return self.api_query('returnOrderTrades',{"orderNumber":orderNumber})

    def returnBalances(self):
    	return self.api_query('returnBalances')
    
    
    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". 
    # If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs: 
    # orderNumber   The order number
    def buy(self,currencyPair,rate,amount):
        return self.api_query('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})
        
            # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". 
    # If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs: 
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

import sys
testapi = poloniex(pkey,spkey)
def usage():
	print "Usage: "+sys.argv[0]+" currencyPair type rate amount"
	print '"currencyPair": "BTC_XVC" <== in this format!!'
	print '"type": "buy" or "sell"'
	print '"rate": "0.00018500" <== with dot!!, desired exchange rate for the coin'
	print '"amount": "all" or "455.34206390" <== number of the coins'
	sys.exit(0)

print sys.argv
if len(sys.argv) != 5:
	usage()
if sys.argv[2] not in ['buy','sell']:
	usage()
type=sys.argv[2]
if '.' not in sys.argv[3]:
	usage()
rate=sys.argv[3]
if '_' not in sys.argv[1]:
	usage()
currencyPair=sys.argv[1]
mainCurrency=currencyPair.split('_')[0]
if sys.argv[4] =='all':
	print 'Please wait, getting balances from Poloniex ....',
	balances = testapi.returnBalances()[mainCurrency]
	print 'done!'
	print('Current '+mainCurrency+' balance: '+str(balances))
	amount=float(balances)/float(rate)	
else:
	amount=sys.argv[4]
print('Amount of '+currencyPair.split('_')[1]+' to '+type+': '+'{:.8f}'.format(float(amount)))
if type=='buy':
    orders = testapi.buy(currencyPair,'{:.8f}'.format(float(rate)),'{:.8f}'.format(float(amount)))
else:    
    orders = testapi.sell(currencyPair,'{:.8f}'.format(float(rate)),'{:.8f}'.format(float(amount)))
if orders!='':
	print('Resulting orders: '+orders)
