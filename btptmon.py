#!/usr/bin/python
import imp, sys, pip, time, thread, traceback, requests
def install(package):
    pip.main(["install", package])
try:
    imp.find_module("bittrex")
except ImportError:
    print "The 'bittrex' package is not installed. Attempting to install..."
    install("bittrex")
import bittrex
from datetime import datetime
from requests import Session
from signalr import Connection

#theCode
VOLUME_LIMIT = 300.0

btr = bittrex.Bittrex('','')
tick = "https://www.poloniex.com/public?command=returnTicker"

while True:
    print(str(datetime.now()))
# Bittrex
    print('='*49)
    print('Bittrex pairs for 24 hrs over '+str(VOLUME_LIMIT)+' volume limit')
    print('='*49)
    bpairscount = 0
    try:
        r = btr.get_market_summaries()
    except ConnectionError:
        print("Connection error, waiting a little.")
        time.sleep(1)
        continue
    except ValueError:
        print "[X] Error getting market summary."
    if r["success"]:
        res = r["result"]
        for market in res:
            mname = market["MarketName"]
            vol = float(market["BaseVolume"])
            last = float(market["Last"])
            if last == 0:
                continue
            if mname.startswith('BTC') and vol >= VOLUME_LIMIT:
                bpairscount += 1
                print(str(mname).ljust(11)+' with BTC volume: '+str( market["BaseVolume"]).rjust(20))
    else:
        print(str(r))
    print('Found '+str(bpairscount)+' pairs on Bittrex ...')
# Polo
    print('='*49)
    print ('Poloniex pairs for 24 hrs over '+str(VOLUME_LIMIT)+' volume limit')
    print('='*49)
    ppairscount = 0
    try:
        t=requests.get(tick).json()
    except SSLError:
        print('Polo certificate verification failed\n')
        continue
    except ConnectionError:
        print('Connection to %s failed!\n' % tick)
        continue
    except InvalidSchema as e:
        print('%s\n' % e)
        continue
    except:
        print('Polo laggz ...\n')
        continue
    for i,k in t.items():
        if i.startswith('BTC') and float(t[i]["baseVolume"])>= VOLUME_LIMIT:
            ppairscount += 1
            print(str(i).ljust(11)+' with BTC volume: '+str(float(t[i]["baseVolume"])).rjust(20))
    print('Found '+str(ppairscount)+' pairs on Poloniex ...')
    time.sleep(2.92)
