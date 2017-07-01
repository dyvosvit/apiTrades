#generate new API key/secret from Bittrex and put them here
#it worked for you, you use and like it = donate any amount you wish
#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

key = ""
skey= ""

import urllib
import time
import hmac
import hashlib
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError
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
        #print(options)
        request_url += urlencode(options)

        signature = hmac.new(self.api_secret, request_url, hashlib.sha512).hexdigest()

        headers = {"apisign": signature}

        ret = requests.get(request_url, headers=headers)
        return ret.json()

    def get_markets(self):
        return self.api_query('getmarkets')

    def get_currencies(self):
        return self.api_query('getcurrencies')

    def get_ticker(self, market):
         return self.api_query('getticker', {'market': market})

    def get_market_summaries(self):
        return self.api_query('getmarketsummaries')

    def get_orderbook(self, market, depth_type, depth=20):
        return self.api_query('getorderbook', {'market': market, 'type': depth_type, 'depth': depth})

    def get_market_history(self, market, count):
        return self.api_query('getmarkethistory', {'market': market, 'count': count})

    def buy_market(self, market, quantity, rate):
        return self.api_query('buymarket', {'market': market, 'quantity': quantity, 'rate': rate})

    def buy_limit(self, market, quantity, rate):
        return self.api_query('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def sell_market(self, market, quantity, rate):
        return self.api_query('sellmarket', {'market': market, 'quantity': quantity, 'rate': rate})

    def sell_limit(self, market, quantity, rate):
       return self.api_query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def cancel(self, uuid):
       return self.api_query('cancel', {'uuid': uuid})

    def get_open_orders(self, market):
        return self.api_query('getopenorders', {'market': market})

    def get_balances(self):
       return self.api_query('getbalances', {})

    def get_balance(self, currency):
        return self.api_query('getbalance', {'currency': currency})

    def get_deposit_address(self, currency):
       return self.api_query('getdepositaddress', {'currency': currency})

    def withdraw(self, currency, quantity, address):
        return self.api_query('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})

    def get_order(self, uuid):
       return self.api_query('getorder', {'uuid': uuid})

    def get_order_history(self, market = ""):
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
def printFancyHeader():
    print('===========================================================================================')
    print('==     ========  =====        ====        ====       ======       ====  =====  ============')
    print('==  ===  ======  ========  ==========  =======  ====   ====  ==========  ===  =============')	
    print('==  == ========  ========  ==========  =======       ======       ======    ===============')	
    print('==  ====  =====  ========  ==========  =======  ====  =====  ==========  ===  =============')	
    print('==     ========  ========  ==========  =======  ======  ===       ====  =====  ============')
    print('===========================================================================================')	

def f(a,n,s):
    return (s+str(format(a, '.8f'))).rjust(n)
def pollBittrexTrades():
    resultMarkets=testapi.get_order_history()
    #print(resultMarkets)
    if resultMarkets['success']==True:
        for i in resultMarkets['result'][:latestTrades]:
            #print(i)
            text_out=str(i['Exchange']).ljust(9)
            text_out=text_out+str(i['TimeStamp']).replace('T',' ').split('.')[0].ljust(20)+str(i['OrderType'][6:]).ljust(5)
            text_out=text_out+'of '+f(i['Quantity'],8,'')+' '+str(i['Exchange'][4:]).ljust(4)
            text_out=text_out+' at '+f(i['PricePerUnit'],9,'')+', with revenue '
            if i['OrderType'][6:] == 'BUY':
                print(RED+text_out+f(i['Price'],12,'-')+ENDC)
            else:
                print(GREEN+text_out+f(i['Price'],12,'+')+ENDC)
def calculateEstimatedBTCs(balanceBTC):
    resultBalances=testapi.get_balances()
    bittrexCoinz={}
    if resultBalances['success']==True:
        print 'Active coins on Bittrex: ',
        for i in resultBalances['result']:
            if (i['Balance']!=0):
                bittrexCoinz[i['Currency']]=i
                print i['Currency'],
    print
    resultTicker=testapi.get_market_summaries()
#    bittrexPrices={}
    totalRevenues=0
    if resultTicker['success']==True:
        for i in resultTicker['result']:
            market,coin =  i['MarketName'].split('-')
            if (market=='BTC') and (coin in bittrexCoinz.keys()):
#                bittrexPrices[coin]={'Last':i['Last'],'Bid':i['Bid'],'Ask':i['Ask'],'uuid':''}
                #print bittrexCoinz, market, coin
                totalRevenues += bittrexCoinz[coin]['Balance']*i['Last']
    return balanceBTC+totalRevenues

while (True):
    cls()
    printFancyHeader()
    balance=testapi.get_balance('BTC')['result']
    print 'Current available BTC balance is:                {:+.14f}'.format(balance['Available'])
    estim = calculateEstimatedBTCs(balance['Available'])
    print 'Current estimated value of portfolio in BTCs (lastprice):{:+.14f}'.format(float(estim))
    #print([i['Available'] for i in balance if i['Currency']==u'BTC'][0])
    pollBittrexTrades()
    print('Waiting for next ',pollingInterval,' seconds')
    time.sleep(pollingInterval)
