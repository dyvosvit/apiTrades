#P O L O N I E X TRADE HISTORY 5 CRIPTONAUTA - Fancy Title + colors + prices + balance + deposits + profit !!!!!
#by Prof. @Dyvosvit
#

#it worked for you, you use and like it = donate any amount you wish
#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

#generate new API key/secret from Poloniex and put them here
pkey = ''
spkey = ''
#generate new API key/secret from Poloniex and put them here

apidelay = 0.888
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

    def returnDW(self):
        return self.api_query("returnDepositsWithdrawals",{'start': '0', 'end': time.time()})

    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})

    def returnBalances(self):
        return self.api_query('returnBalances')

    def returnCompleteBalances(self):
        return self.api_query('returnCompleteBalances')

    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})

    def returnTradeHistory(self,currencyPair):
        return self.api_query('returnTradeHistory',{"currencyPair":currencyPair})


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

# depends on completeBalances
def poloTotalBTC():
   totalBTC = 0
   for i in completeBalances:
      totalBTC+=float(completeBalances[i]['btcValue'])
   return totalBTC

# depends on completeBalances
def poloActiveBalances():
    polo_balances = {}
    for stock, balances in completeBalances.items():
        for balance_type, value in balances.items():
            if float(value) > 0:
                polo_balances[stock] = balances
    return polo_balances

deposits, withdrawals = {}, {}

def poloDWhistory():
    historyDW=testapi.returnDW()
    if historyDW=='':
        return ''
    for deposit in historyDW['deposits']:
        if deposit['currency'] in deposits:
            deposits[deposit['currency']] += float(deposit['amount'])
        else:
            deposits[deposit['currency']] = float(deposit['amount'])
    for withdrawal in historyDW['withdrawals']:
        if withdrawal['currency'] in withdrawals:
            withdrawals[withdrawal['currency']] += float(withdrawal['amount'])
        else:
            withdrawals[withdrawal['currency']] = float(withdrawal['amount'])
    return deposits, withdrawals
# depends on poloTicker
def poloTickerPrice(ticker):
    try:
        return float(poloTicker[ticker]["last"])
    except KeyError:
        return 0

# depends on poloTicker, deposits, withdraws, poloTickerPrice
def poloBTCbalance(ticker):
    balance = 0
    for deposit_ticker, amount in deposits.items():
        if deposit_ticker != u'BTC':
            balance += amount * poloTickerPrice(deposit_ticker)
        else:
            balance += amount
    for withdrawal_ticker, amount in withdrawals.items():
        if withdrawal_ticker != u'BTC':
            balance -= amount * poloTickerPrice(withdrawal_ticker)
        else:
            balance -= amount
    return balance

while (True):
    cls()
    print 'Showing latest '+str(latestTrades)+ ' trades'
    completeBalances = testapi.returnCompleteBalances()
    time.sleep(apidelay)
    poloCurrentBalance=poloTotalBTC()#current
    if completeBalances != '':
        print 'Current BTC balance: available ', completeBalances['BTC']['available'],' on orders: ',completeBalances['BTC']['onOrders'],' totalling ',completeBalances['BTC']['btcValue']
        print 'Current estimated value of portfolio in BTCs:     ', poloCurrentBalance
        time.sleep(apidelay)
        poloActiveCoins = poloActiveBalances()
        print 'Current active coin balances on Polo: ' + ' '.join(poloActiveCoins)
        poloDWhistory() # fills deposits/withdraws sets
        if deposits != {}:
            for currency, deposit in deposits.items():
                withdrawal = withdrawals[currency] if currency in withdrawals else 0
                print('Deposits - Withdrawals:               {} = {} - {} = {}'.format(currency, deposit, withdrawal, deposit - withdrawal))
                time.sleep(apidelay)
            poloTicker = testapi.returnTicker()
            poloBalance = poloBTCbalance(poloTicker)
            print 'Current profit is '+ '{:.4}%'.format(poloCurrentBalance / poloBalance * 100)+ '              Pure profit is ' + '{:.12}'.format(poloCurrentBalance - poloBalance)
    time.sleep(3*apidelay)
    pollCoinsTrades24h()
    print 'Waiting for next '+str(pollingInterval)+' seconds'
    time.sleep(pollingInterval)
