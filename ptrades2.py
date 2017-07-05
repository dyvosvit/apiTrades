#by Prof. @Dyvosvit
#
# 1. install python 2.7.X
# during install tick add python to PATH
# 2. run in cmd (Win+R)
# c:\python27\python -m pip install colorama
# 3. copy script to c:\python27 folder
# 4. run in cmd (Win+R)
# c:\python27\python ptrades2.py

#it worked for you, you use and like it = donate any amount you wish
#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

#generate new API key/secret from Poloniex and put them here
pkey = ''
spkey = ''
#generate new API key/secret from Poloniex and put them here

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import Request, urlopen, URLError, HTTPError
    from urllib import urlencode

import json
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
            #print(req)
            try:
                ret = urlopen(Request('https://poloniex.com/tradingApi', post_data, headers))
            except URLError as e:
                print("Polo is lagging, we've got some error")
                print(e.code,e.reason)
                print("  ... continue")
                return ''

            jsonRet = json.loads(ret.read())

            return self.post_process(jsonRet)


    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24Volume(self):
        return self.api_query("return24Volume")

    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})


    # Returns all of your balances.
    # Outputs: 
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def returnBalances(self):
        return self.api_query('returnBalances')
    
    def returnCompleteBalances(self):
        return self.api_query('returnCompleteBalances')
    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})


    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def returnTradeHistory(self,currencyPair):
        return self.api_query('returnTradeHistory',{"currencyPair":currencyPair})

#from poloniex import Poloniex
import colorama
from colorama import Fore, Back, Style
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
colorama.init()
testapi = poloniex(pkey,spkey)
check_coins = 'currencies.txt'
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

def pollCoinsTrades24h():
    print_coins = []
    tradeHistory24h = testapi.returnTradeHistory('All')
    try:
        with open(check_coins, 'r') as afile:
            for coin in afile:
                print_coins += [coin.strip()]
    except:
        if print_coins == []:
            print_coins = 'ETH XRP XEM LTC STR  BCN ETC DGB SC BTS DOGE DASH GNT EMC2 STEEM XMR ARDR STRAT NXT  ZEC LSK  FCT GNO NMC MAID   BURST GAME  DCR  SJCX RIC FLO REP NOTE CLAM SYS PPC EXP XVC VTC FLDC LBC AMP POT NAV XCP  BTCD  RADS   PINK GRC  NAUT  BELA  OMNI HUC NXC VRC  XPM VIA PASC  BTM NEOS XBC  BLK SBD BCY'
            print_coins = print_coins.strip().split()
    work_set = {}
    for line in tradeHistory24h:
        if line[4:] in print_coins:
            for element in tradeHistory24h[line]:
                signd = '-' if element['type']=='buy' else '+'
                totald = signd+element['total']
                thetext = 'with investments of' if element['type']=='buy' else 'with revenue of'
                work_set[int(element['globalTradeID'])]=['BTC_'+line[4:], element['date'],element['type'].upper(), 'of',line[4:] , 'at', element['rate'],thetext,totald]
    for key in sorted(work_set.keys(),reverse=True)[:latestTrades]:
        colorit = RED if work_set[key][2] == 'BUY' else GREEN
        print(colorit+' '.join(work_set[key])+ENDC)
while (True):
    cls()
    print 'Showing latest '+str(latestTrades)+ ' trades'
    balance = testapi.returnBalances()
    estimatedBalance = testapi.returnCompleteBalances()
    if balance != '':
       print 'Current available BTC: ', balance['BTC'].rjust(36)
       if estimatedBalance!= '':
           estim = 0
           for i in estimatedBalance:
               estim+=float(estimatedBalance[i]['btcValue'])
           print 'Current estimated value of portfolio in BTCs:    ', estim
    pollCoinsTrades24h()
    print 'Waiting for next '+str(pollingInterval)+' seconds'
    time.sleep(pollingInterval)
