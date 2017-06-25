#generate new API key/secret from Bittrex and put them here
#it worked for you, you use and like it = donate any amount you wish

#BTC: 1HRjjHByNL2enV1eRR1RkN698tucecL6FA
#ETH: 0x4e5e7b86baf1f8d6dfb8a242c85201c47fa86c74
#ZEC: t1aKAm7qXi6fbGvAhbLioZm3Q8obb4e3BRo

#'last' or 'highestBid' or 'lowestAsk' or 'average' or 'bid+1' or 'last-1'
sellmodes={'1':'last','2':'highestBid','3':'lowestAsk','4':'average','5':'bid+1','6':'last-1'}

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
            except HTTPError as e:
                print("Polo is lagging, we've got "+str(e.code)+" error  ... continue")
                print(e.read())
                return ''
            except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
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
        
 # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The currency pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # Outputs: 
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

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

def poloSellTotalBTC(price):
    poloSell = 0
    for i in completeBalances:
    	#print poloTickerPrice(i,price),
        if i != u'BTC'and float(completeBalances[i]['btcValue'])>0:
            poloSell+=float(completeBalances[i]['available'])*poloTickerPrice('BTC_'+i,price)
            poloSell+=float(completeBalances[i]['onOrders'])*poloTickerPrice('BTC_'+i,price)
    return poloSell
   
   
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
def pF(f):
	return float('{0:.8f}'.format(f))
	
# depends on poloTicker
def poloTickerPrice(ticker,price=sellmodes['1']):
    try:
    	if price=='average':
    		return pF((float(poloTicker[ticker]['highestBid'])+float(poloTicker[ticker]['lowestAsk']))/2.0)
    	elif price=='bid+1':
    		return pF((float(poloTicker[ticker]['highestBid'])+0.00000001))
    	elif price=='last-1':
    		return pF((float(poloTicker[ticker]['last'])-0.00000001))
        return float(poloTicker[ticker][price])
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
sellOrders={}
def dumpPoloniex():
    poloTicker=testapi.returnTicker()
    for ticker,pricedata in poloTicker.items():
    	#print ticker
    	if ticker.split('_')[1] in poloActiveCoins:
    		print(ticker,pricedata['last'],pricedata['highestBid'],pricedata['lowestAsk'],
    		poloTickerPrice(ticker,price='average'),poloTickerPrice(ticker,price='bid+1'),
    		poloTickerPrice(ticker,price='last-1'))
    for num, mode in sellmodes.items():
    	print num,' = ', mode
    	s1 = float(poloSellTotalBTC(mode))
    	s2 = float(completeBalances['BTC']['available'])
    	print mode,s1,'+',s2,'=',s1+s2,' diff to Polo estimated: ', pF(s1+s2-poloCurrentBalance)
    selectedMode = raw_input('Select Sell Mode: ')
    for tick in poloActiveCoins:
    	print(tick, poloActiveCoins[tick])
    	market = 'BTC_'+tick
    	price = poloTickerPrice(market,price=sellmodes[selectedMode])
    	coins = float(poloActiveCoins[tick]['available'])
    	print(market,pF(price),pF(coins),price*coins)
    	time.sleep(apidelay)
    	sellOrders[tick] = testapi.sell(market,"{0:.8f}".format(price),"{0:.8f}".format(coins))
    	print sellOrders[tick]
    
while (True):
    cls()
    completeBalances = testapi.returnCompleteBalances()
    #print completeBalances
    time.sleep(apidelay)
    poloCurrentBalance=poloTotalBTC()#current
    if completeBalances != '':
        print 'Current BTC balance: available ', completeBalances['BTC']['available'],' on orders: ',completeBalances['BTC']['onOrders'],' totalling ',completeBalances['BTC']['btcValue']
        print 'Current estimated value of portfolio in BTCs:     ', poloCurrentBalance
        time.sleep(apidelay)
        poloActiveCoins = poloActiveBalances()
        if 'BTC' in poloActiveCoins:
        	del poloActiveCoins['BTC']
        print 'Current active coin balances on Polo: ' + ' '.join(poloActiveCoins)
        poloDWhistory() # fills deposits/withdraws sets
        if deposits != {}:
            poloTicker = testapi.returnTicker()
            time.sleep(apidelay)
            poloBalance = poloBTCbalance(poloTicker)
            print 'Current profit is '+ '{:.4}%'.format(poloCurrentBalance / poloBalance * 100)+ '              Pure profit is ' + '{:.12}'.format(poloCurrentBalance - poloBalance)
    time.sleep(3*apidelay)
    dumpPoloniex()
    print 'Waiting for next '+str(pollingInterval)+' seconds'
    time.sleep(pollingInterval)
