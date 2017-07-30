#generate new API key/secret from Poloniex and put them here
#it worked for you, you use and like it = donate any amount you wish
#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

pkey = ''

spkey= ''


apidelay = 0.888
poll = 10
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
import calendar
import hmac,hashlib

import socket
socket.setdefaulttimeout(30)

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
        print('running command: '+command)
		#time.sleep(apidelay)
		
        if(command == "returnTicker" or command == "return24Volume" or command == "returnCurrencies"):
            try:
            	ret = urlopen(Request('https://poloniex.com/public?command=' + command))
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
            #if debug_print :
            #	print(req)
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

    def returnTicker(self):
    	return self.api_query('returnTicker')

    def returnChartData(self,currencyPair,period,start,end):
        return self.api_query('returnChartData',{"currencyPair":currencyPair,'period':period,'start':start,'end':end})
        
        
import sys

def fkntime(weeks=0,days=0,hours=0,minutes=0):
	return str(time.mktime((datetime.datetime.now()-datetime.timedelta(weeks=weeks,days=days,hours=hours,minutes=minutes)).timetuple())).split('.')[0]

f=float

import sys
import fileinput

filetoedit='ALLPAIRS-params.js'

testapi = poloniex(pkey,spkey)

def setsg(lvl1,lvl2,lvl3):
	for i, line in enumerate(fileinput.input(filetoedit, inplace=1)):
		if 'BUYLVL1' in line:
			sys.stdout.write('BUYLVL1: '+str(lvl1)+',\n')
		elif 'BUYLVL2' in line:
			sys.stdout.write('BUYLVL2: '+str(lvl2)+',\n')
		elif 'BUYLVL3' in line:
			sys.stdout.write('BUYLVL3: '+str(lvl3)+',\n')
		else:
			sys.stdout.write(line)

while True:
	print 75*'*'
	print datetime.datetime.fromtimestamp(time.time()),
	ticker=100*f(testapi.returnTicker()['USDT_BTC']['percentChange'])
	print 'Current ticker USDT_BTC price change in 24hr (in %):',ticker
	#btc INCREASE in 24 hour 4% or more
	#set BUY SG to 3/15/99
	if ticker >= 4.0:
		print 'btc INCREASE in 24 hour 4% or more'
		print 'set BUY SG to 3/15/99'
		setsg(3,15,99)
	#btc dropped in 24 hours 6% or more
	#set BUY SG to 8/15/99
	elif ticker<=-6.0:
		print 'btc dropped in 24 hours 6% or more'
		print 'set BUY SG to 8/15/99'
		setsg(8,15,99)
	chartData=testapi.returnChartData('USDT_BTC',300,fkntime(hours=1),fkntime())['candleStick']
	start = chartData[0]['weightedAverage']
	stop =  chartData[-1]['weightedAverage']
	difference1hr = (stop-start)/start*100.0
	print 'Weighted price an hour ago:', start,'now:',stop,'diff: {:.3f} %'.format(difference1hr)
	if difference1hr<=-4.0:
		print 'btc dropped in 1 hour 4% or more'
		print 'set BUY SG to 4/15/99'
		setsg(4,15,99)
	#btc dropped in 1 hour 4% or more
	#set BUY SG to 4/15/99
	elif difference1hr>=4.0:
		print 'btc INCREASE in 1 hour 4% or more'
		print 'set BUY SG to 2/15/99'
	#btc INCREASE in 1 hour 4% or more
	#set BUY SG to 2/15/99
		setsg(2,15,99)
	print 'Wait',poll,'seconds'
	time.sleep(poll)