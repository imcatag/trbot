from binance.spot import Spot as CL
from binance.error import ClientError
from binance.lib.utils import config_logging
import websocket, json, pprint
from tabulate import tabulate
import time
import math

start = time.time()

testfile = open("test.txt", "r")
realfile = open("real.txt", "r")

testkey = testfile.readline() 
testsecret = testfile.readline() 

realkey = realfile.readline()
realsecret = realfile.readline()

coin = 'ETHUSDT'

def wsopen(ws):
    print('opened connection')

def wsclose(ws):
    print('closed connection')

def wsmsg(ws, message):
    print('recieved message')
    json_message = json.loads(message)
    pprint.pprint(type(json_message))
    candle = json_message['k']
    close = candle['c']
    #high = candle['h']
    #low = candle['l']
    #vol = candle['v']
    closedcandle = candle['x']
    """
    TO DO LIST:
    SEE IF LAST TRADE OF SELECTED COIN WAS BUY OR SELL AND USDT AVAILABLE
    IF LAST IS BUY
        
        IF CURRENT PROFIT > 99% MAX PROFIT AND CURRENT PROFIT > (100 + 90% * TAKE PROFIT) * BUY PRICE
            CURRENT PROFIT = MAX (CURRENT PROFIT, MAX PROFIT)
        ELSE
            STOP AT -3% STOP LOSS
            STOP IF AVG25 CURVE IS ABOVE GRAPH
            STOP ON SHOCK DROP
    
    ELSE
        IF PRICE > 101% * AVG25 AND AVG25 WAS > PRICE FOR 1 CANDLE END IN THE CURRENT SESSION AFTER LAST SELL
            BUY


    """




def printas():
    crs = client.account()['balances']


    assets = []
    table = []

    for i in crs:
        if float(i['free']) > 0.0000001:
            assets = []
            assets.append(i['asset'])
            assets.append(i['free'])
            assets.append(i['locked'])
            table.append(assets)


    headers = ['ASSET', 'FREE', 'LOCKED']
    print('\n')
    print (tabulate(table,headers, tablefmt="psql"))

socket = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

ws = websocket.WebSocketApp(socket, on_open = wsopen, on_close = wsclose, on_message = wsmsg)

testnet = True

client = CL(testkey, testsecret, base_url='https://testnet.binance.vision')

while(True):
    
    print('\ncoin pair' , coin)
    if testnet:
        print('using test server')
        
    else:
        print('USING REAL SERVER!!!')

    whattodo = input("type help for help\n\n> ").lower().strip()

    if whattodo == 'help':
        print('\nstart to start\nCtrl+C to stop\ntestserver to switch to test server\nrealserver to switch to real server\nbal/ls/assets to check assets\ncrypto/cc/cr to change crypto pair\ntime for server time\nexit/quit to exit')

    elif whattodo == 'as' or whattodo == 'ls' or whattodo == 'assets':
        printas()

    elif whattodo == 'testserver' or whattodo == 'test':
        testnet = True
        client = CL(testkey, testsecret, base_url='https://testnet.binance.vision')
    
    elif whattodo == 'realserver':
        if(input('Type CONFIRM in ALL CAPS to switch to REAL SERVER: ')) == 'CONFIRM':
            testnet = False
            client = CL(realkey, realsecret, base_url='https://api1.binance.com')

    elif whattodo == 'time':
        print(client.time())

    elif whattodo == 'start':
        ws.run_forever()

    elif whattodo == 'exit' or whattodo == 'quit' or whattodo == 'q':
        break

    elif whattodo == 'crypto' or whattodo == 'cr' or whattodo == 'cc':
        coin = input('Type your crypto pair: ').upper().strip()
        socket = 'wss://stream.binance.com:9443/ws/'+ coin.lower() +'@kline_5m'
        ws = websocket.WebSocketApp(socket, on_open = wsopen, on_close = wsclose, on_message = wsmsg)

    elif whattodo == 'yo':
        print('\nyo')

    else:
        print('\nwhat\n')


print('')

stop = time.time()
sec = math.trunc(stop - start)
if(sec > 1):
    hr = sec // 3600
    mn = sec // 60
    sec = sec % 60
    if hr:
        print('bot ran for ', hr, 'h ', mn, 'm ', sec, 's', sep = '')
    elif mn:
        print('bot ran for ', mn, 'm ', sec, 's', sep = '')
    else:
        print('bot ran for ', sec, 's', sep = '')

print('cya')