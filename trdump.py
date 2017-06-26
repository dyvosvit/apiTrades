#generate new API key/secret from Bittrex and put them here
#it worked for you, you use and like it = donate any amount you wish
#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo
#'Last' or 'Bid' or 'Ask'

sellmode='Bid'
key = ""
skey= ""

import urllib
import time
import hmac
import hashlib
try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urljoin
import requests
import json

BUY_ORDERBOOK = 'buy'
SELL_ORDERBOOK = 'sell'
BOTH_ORDERBOOK = 'both'

PUBLIC_SET = ['getmarkets', 'getcurrencies', 'getticker', 'getmarketsummaries', 'getorderbook',
			  'getmarkethistory']

MARKET_SET = ['getopenorders', 'cancel', 'sellmarket', 'selllimit', 'buymarket', 'buylimit']

ACCOUNT_SET = ['getbalances', 'getbalance', 'getdepositaddress', 'withdraw', 'getorder', 'getorderhistory', 'getwithdrawalhistory', 'getdeposithistory']


class Bittrex(object):

	def __init__(self, api_key, api_secret):
		self.api_key = str(api_key) if api_key is not None else ''
		self.api_secret = str(api_secret) if api_secret is not None else ''
		self.public_set = set(PUBLIC_SET)
		self.market_set = set(MARKET_SET)
		self.account_set = set(ACCOUNT_SET)

	def api_query(self, method, options=None):
		"""
		Queries Bittrex with given method and options
		:param method: Query method for getting info
		:type method: str
		:param options: Extra options for query
		:type options: dict
		:return: JSON response from Bittrex
		:rtype : dict
		"""
		if not options:
			options = {}
		nonce = str(int(time.time() * 1000))
		base_url = 'https://bittrex.com/api/v1.1/%s/'
		request_url = ''

		if method in self.public_set:
			request_url = (base_url % 'public') + method + '?'
		elif method in self.market_set:
			request_url = (base_url % 'market') + method + '?apikey=' + self.api_key + "&nonce=" + nonce + '&'
		elif method in self.account_set:
			request_url = (base_url % 'account') + method + '?apikey=' + self.api_key + "&nonce=" + nonce + '&'
		print(request_url,options)
		request_url += urlencode(options)

		signature = hmac.new(self.api_secret, request_url, hashlib.sha512).hexdigest()

		headers = {"apisign": signature}

		ret = requests.get(request_url, headers=headers)
		return ret.json()

	def get_markets(self):
		"""
		Used to get the open and available trading markets
		at Bittrex along with other meta data.
		:return: Available market info in JSON
		:rtype : dict
		"""
		return self.api_query('getmarkets')

	def get_currencies(self):
		"""
		Used to get all supported currencies at Bittrex
		along with other meta data.
		:return: Supported currencies info in JSON
		:rtype : dict
		"""
		return self.api_query('getcurrencies')

	def get_ticker(self, market):
		"""
		Used to get the current tick values for a market.
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str
		:return: Current values for given market in JSON
		:rtype : dict
		"""
		return self.api_query('getticker', {'market': market})

	def get_market_summaries(self):
		"""
		Used to get the last 24 hour summary of all active exchanges
		:return: Summaries of active exchanges in JSON
		:rtype : dict
		"""
		return self.api_query('getmarketsummaries')

	def get_orderbook(self, market, depth_type, depth=20):
		"""
		Used to get retrieve the orderbook for a given market
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str
		:param depth_type: buy, sell or both to identify the type of orderbook to return.
			Use constants BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
		:type depth_type: str
		:param depth: how deep of an order book to retrieve. Max is 100, default is 20
		:type depth: int
		:return: Orderbook of market in JSON
		:rtype : dict
		"""
		return self.api_query('getorderbook', {'market': market, 'type': depth_type, 'depth': depth})

	def get_market_history(self, market, count):
		"""
		Used to retrieve the latest trades that have occured for a
		specific market.
		/market/getmarkethistory
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str
		:param count: Number between 1-100 for the number of entries to return (default = 20)
		:type count: int
		:return: Market history in JSON
		:rtype : dict
		"""
		return self.api_query('getmarkethistory', {'market': market, 'count': count})

	def sell_market(self, market, quantity, rate):
		"""
		Used to place a sell order in a specific market. Use sellmarket to place
		market orders. Make sure you have the proper permissions set on your
		API keys for this call to work
		/market/sellmarket
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str
		:param quantity: The amount to purchase
		:type quantity: float
		:param rate: The rate at which to place the order.
			This is not needed for market orders
		:type rate: float
		:return:
		:rtype : dict
		"""
		return self.api_query('sellmarket', {'market': market, 'quantity': quantity, 'rate': rate})

	def sell_limit(self, market, quantity, rate):
		"""
		Used to place a sell order in a specific market. Use selllimit to place
		limit orders Make sure you have the proper permissions set on your
		API keys for this call to work
		/market/selllimit
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str
		:param quantity: The amount to purchase
		:type quantity: float
		:param rate: The rate at which to place the order.
			This is not needed for market orders
		:type rate: float
		:return:
		:rtype : dict
		"""
		return self.api_query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

	def cancel(self, uuid):
		"""
		Used to cancel a buy or sell order
		/market/cancel
		:param uuid: uuid of buy or sell order
		:type uuid: str
		:return:
		:rtype : dict
		"""
		return self.api_query('cancel', {'uuid': uuid})

	def get_open_orders(self, market):
		"""
		Get all orders that you currently have opened. A specific market can be requested
		/market/getopenorders
		:param market: String literal for the market (ie. BTC-LTC)
		:type market: str
		:return: Open orders info in JSON
		:rtype : dict
		"""
		return self.api_query('getopenorders', {'market': market})

	def get_balances(self):
		"""
		Used to retrieve all balances from your account
		/account/getbalances
		:return: Balances info in JSON
		:rtype : dict
		"""
		return self.api_query('getbalances', {})

	def get_balance(self, currency):
		"""
		Used to retrieve the balance from your account for a specific currency
		/account/getbalance
		:param currency: String literal for the currency (ex: LTC)
		:type currency: str
		:return: Balance info in JSON
		:rtype : dict
		"""
		return self.api_query('getbalance', {'currency': currency})

	def get_order(self, uuid):
		"""
		Used to get an order from your account
		/account/getorder
		:param uuid: The order UUID to look for
		:type uuid: str
		:return:
		:rtype : dict
		"""
		return self.api_query('getorder', {'uuid': uuid})

	def get_order_history(self, market = ""):
		"""
		Used to retrieve your order history
		/account/getorderhistory
		:param market: Bittrex market identifier (i.e BTC-DOGE)
		:type market: str
		:return:
		:rtype : dict
		"""
		if market == "":
			return self.api_query('getorderhistory')
		else:
			return self.api_query('getorderhistory', {"market": market})


testapi = Bittrex(key,skey)
import colorama
from colorama import Fore, Back, Style
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
colorama.init()
pollingInterval = raw_input('How often should we poll trades? (default: 30 seconds)')
if pollingInterval == '':
    pollingInterval = 30
else:
    pollingInterval = int(pollingInterval)
latestTrades = raw_input('How many trades should we see? (default: 30 trades)')
if latestTrades == '':
    latestTrades = 30
else:
    latestTrades = int(latestTrades)
RED= '\033[91m'
GREEN='\033[92m'
ENDC='\033[0m'

def f(a,n,s):
	return (s+str(format(a, '.8f'))).rjust(n)
def dumpBittrex():
	# get BTC balance before
	# for testing purposes
	resultMarkets=testapi.get_balance('BTC')
	if resultMarkets['success']==True:
		print('BTC balance before dump was: ' + str(resultMarkets['result']['Available']))
    #get non-zero coins available
	resultBalances=testapi.get_balances()
	dumpCoinz={}
	if resultBalances['success']==True:
		print('Coins we are going to dump NOW!:')
		for i in resultBalances['result']:
			if (i['Balance']!=0):
			    print i['Currency'],
			    dumpCoinz[i['Currency']]=i
	print
	print('Overall, we have to sell: ' + str(len(dumpCoinz))+' coins.')
	#for i in dumpCoinz.values():
	#	print(i['Currency'],i['Available'])
	# get prices for the coins we have
	resultTicker=testapi.get_market_summaries()
	print(len(dumpCoinz.keys()))
	dumpPrices={}
	if resultTicker['success']==True:
		#print(len(resultTicker['result']))
		for i in resultTicker['result']:
			if (i['MarketName'][:3]=='BTC') and (i['MarketName'][4:] in dumpCoinz.keys()):
			    dumpPrices[i['MarketName'][4:]]={'Last':i['Last'],'Bid':i['Bid'],'Ask':i['Ask'],'uuid':''}
			    #print(i['MarketName'][3:])
	print(len(dumpPrices.keys()))
	coin, market, quantity, rate, revenue ='','',0,0,0
	totalRevenues=0
	for i in dumpPrices.keys():
		coin, market, quantity = i, 'BTC-'+i, dumpCoinz[i]['Available'], 
		rate, revenue = dumpPrices[i][sellmode], dumpCoinz[i]['Available']*dumpPrices[i][sellmode]
		print('Selling '+str(quantity)+' of '+coin+' on '+market+' market for '+str(rate)+' with revenue of ', revenue)
		resultSell=testapi.sell_limit(market, quantity, rate)
		if resultSell['success']==True:
			print('Sell order for '+i+' coin: UUID is '+resultSell['result']['uuid'])
			dumpPrices[i]['uuid']=resultSell['result']['uuid']
		else:
			print(resultSell)
		totalRevenues+=revenue
	print('We should get '+str(totalRevenues))
	print('with available BTC is should be equal to '+str(resultMarkets['result']['Available']+totalRevenues))

while (True):
    cls()
    # !!! cancel last orders
    dumpBittrex()
    print('Waiting for next ',pollingInterval,' seconds')
    time.sleep(pollingInterval)
