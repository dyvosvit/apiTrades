#generate new API key/secret from Bittrex and put them here
#it worked for you, you use and like it = donate any amount you wish
#need python 27 to run it
# 
# for windows users:
# install python 2.7
# to default folder c:\python27
# fill in api/secret from Bittrex with trade permissions
# copy script to c:\python27
# Press "Start" - run
# c:\python27\python c:\python27\dustkiller.py
# enjoy
#BTC: 1hHa79zoc4REFWFHwMCRQgW7fYPXJHbpf
#ETH: 0x56cbce19cfce6085694457efddcfea604352ab4b
#ZEC: t1doCPW9RW3ZZBjMTV1sq4PrroQZokXyetf

#'Last' or 'Bid' or 'Ask'

pollingInterval = 15
trex_dust_limit = 0.001
key = ""
skey= ""

import datetime, os, time, json
import imp, pip
def install(package):
	pip.main(["install", package])

depends = ['requests', 'openpyxl', 'bittrex']
for i in depends:
	try:
		imp.find_module(i)
	except ImportError:
		print "The '"+i+"' package is not installed. Attempting to install..."
		install(i)

import requests
import json
from bittrex import Bittrex

testapi = Bittrex(key,skey)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def f(a,n,s):
	return (s+str(format(a, '.8f'))).rjust(n)

def dustKiller():
	# get BTC balance before
	# for testing purposes
	resultMarkets=testapi.get_balance('BTC')
	if resultMarkets['success']==True:
		print('BTC balance before dust kill was: ' + str(resultMarkets['result']['Available']))
	else:
		print(resultMarkets)
    #get non-zero coins available
	resultBalances=testapi.get_balances()
	t={}
	if resultBalances['success']==True:
		print 'Coins we have available on balance:', 
		for i in resultBalances['result']:
			b = i['Available']
			if (b!=0) and i['Currency']!='BTC' and i['Currency']!='USDT':
			    print i['Currency'],
			    t[i['Currency']]=i
		print
	# get prices for the coins we have
	resultTicker=testapi.get_market_summaries()
	#print(len(dumpCoinz.keys()))
	dumpPrices={}
	if resultTicker['success']==True:
		#print(len(resultTicker['result']))
		for i in resultTicker['result']:
			if (i['MarketName'][:3]=='BTC') and (i['MarketName'][4:] in t.keys()):
			    dumpPrices[i['MarketName'][4:]]={'Last':i['Last'],'Bid':i['Bid'],'Ask':i['Ask'],'uuidbuy':'','uuidsell':''}
			    #print(i['MarketName'][3:])
#	print t
	dumpCoinz={}		    
	for i in t.keys():
#		print i
#		print t[i]['Available'], dumpPrices[i]['Bid']
#		print t[i]['Available']*dumpPrices[i]['Bid']
#		print t[i]['Available']*dumpPrices[i]['Bid']<trex_dust_limit
		if t[i]['Available']*dumpPrices[i]['Bid']<trex_dust_limit:
			dumpCoinz[i]={}
			dumpCoinz[i]['Available']=t[i]['Available']
	print('Overall, we have to kill dust on ' + str(len(dumpCoinz))+' coins.')
	#print(len(dumpPrices.keys()))
	coin, market, quantity, rate, revenue ='','',0,0,0
	totalRevenues=0
#	print(dumpPrices)
#	print(dumpCoinz)
	for i in dumpCoinz.keys():
		coin, market, quantitySell = i, 'BTC-'+i, dumpCoinz[i]['Available']
		rateBuy = dumpPrices[i]['Ask']
		quantityBuy = trex_dust_limit/dumpPrices[i]['Ask']
		totalBuy = quantityBuy * rateBuy
		print('Buying '+str(quantityBuy)+' of '+coin+' on '+market+' market for '+str(rateBuy)+' with total of ', totalBuy)
		resultBuy=testapi.buy_limit(market, quantityBuy, rateBuy)
		if resultBuy['success']==True:
			print('Buy order for '+i+' coin: trade UUID is '+resultBuy['result']['uuid'])
			dumpPrices[i]['uuidbuy']=resultBuy['result']['uuid']
		else:
			print(resultBuy)
		rateSell = dumpPrices[i]['Bid']
		# change for check balance of coin through api ....
		#quantitySell = quantityBuy + dumpCoinz[i]['Available']
		time.sleep(1)
		quantitySell=testapi.get_balance(i)
		if quantitySell['success']==True:
			quantitySell=quantitySell['result']['Available']
			print(i+' balance now is:', quantitySell)
		totalSell = quantitySell * rateSell
		print('Selling '+str(quantitySell)+' of '+coin+' on '+market+' market for '+str(rateSell)+' with total of ', totalSell)
		resultSell=testapi.sell_limit(market, quantitySell, rateSell)
		if resultSell['success']==True:
			print('Sell order for '+i+' coin: UUID is '+resultSell['result']['uuid'])
			dumpPrices[i]['uuidsell']=resultSell['result']['uuid']
		else:
			print(resultSell)
		totalRevenues+=(totalSell-totalBuy)
	print('Available BTC should be equal to '+str(resultMarkets['result']['Available']+totalRevenues))

while (True):
    #cls()
    dustKiller()
    print('Waiting for next ',pollingInterval,' seconds')
    time.sleep(pollingInterval)
