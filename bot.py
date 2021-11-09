from types import BuiltinMethodType
from binance.spot import Spot as CL
from binance.error import ClientError
from binance.lib.utils import config_logging
import websocket, json, pprint
from tabulate import tabulate
import time
import math

last25 = []
avg25 = []
rsi = []
iscrypto = False
max_profit_percent = 0
cur_price = 0
depth = 0
boughtcandle = False
soldcandle = False
posdiff = []
negdiff = []
avggain = []
avgloss = []

start = time.time()

testfile = open("test.txt", "r")
realfile = open("real.txt", "r")
vassets = open("vassets.txt", "r")

amt = float(vassets.readline().strip())
buy_price = 0

testkey = testfile.readline().strip() 
testsecret = testfile.readline().strip()

realkey = realfile.readline().strip()
realsecret = realfile.readline().strip()

testfile.close()
realfile.close()
vassets.close()


def wsopen(ws):
    print('opened connection')

def wsclose(ws):
    print('closed connection')

def wsmsg(ws, message):
    global cur_price, depth
    #print('recieved message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)
    candle = json_message['k']
    cur_price = float(candle['c'])
    #high = candle['h']
    #low = candle['l']
    #vol = candle['v']
    closedcandle = candle['x']

    global last25, avg25, rsi, posdiff, negdiff, avggain, avgloss
    
    if closedcandle:
        last25.append(cur_price)
        depth += 1
        print(depth)
        if len(last25) > 25:
            last25 = last25[1:]
            avg25.append(sum(last25)/25)
        
        try:
            print(last25[-3], last25[-2],last25[-1])
        except:
            pass
        try:
            print(avg25[-3], avg25[-2],avg25[-1])
        except:
            pass

        boughtcandle = False
        soldcandle = False

        diff = last25[-1] - last25[-2]

        if depth <= 16:
            if diff > 0:
                posdiff.append(diff)
                negdiff.append(0)
            else:
                negdiff.append(abs(diff))
                posdiff.append(0)
            

        if depth == 16:
            negdiff = negdiff[1:]
            posdiff = posdiff[1:]

            avggain.append(sum(posdiff)/14)
            avgloss.append(sum(negdiff)/14)

            rsi.append(100 - (100 / (1 + avggain[-1] / avgloss[-1] )))
 

        if depth > 16:

            if diff > 0:
                avggain.append((avggain[-1] * 13 + diff) / 14)
                avgloss.append((avgloss[-1] * 13) / 14)
            else:
                avgloss.append((avgloss[-1] * 13 + abs(diff)) / 14)
                avggain.append((avggain[-1] * 13) / 14)

            rsi.append(100 - (100 / (1 + avggain[-1] / avgloss[-1] )))

            avgloss = avgloss[1:]
            avggain = avggain[1:]
            
        if len(rsi) > 25:
            rsi = rsi[1:]
            
        print ('\ndiff: ', diff, '\n')
        print ('avggain: ', avggain, '\n')
        print ('avgloss: ', avgloss, '\n')
        print ('rsi: ', rsi, '\n')

    if len(avg25) > 25:
        avg25 = avg25[1:]

    if depth > 16 and closedcandle:
        global iscrypto, amt, buy_price

        if iscrypto:
            if (rsi[-1] >= 72) or (rsi[-2] > 70 and rsi[-1] < 70) or ( ((cur_price - buy_price) / cur_price) > 0.01 and avg25[-1] > last25[-1]):
                amt = amt * cur_price
                print('/ / / / / / / / / sold @ ', cur_price, '\n', amt)
                iscrypto = False
        else:
            if rsi[-2] < 30 and rsi[-1] >=  30:
                print('+ + + + + + + + + bought @ ', cur_price, '\n')
                buy_price = cur_price
                iscrypto = True
                amt = amt / cur_price


    
    """ OLD CONDITIONS
    if depth > 15: #BUYING AND SELLING

        global iscrypto, max_profit_percent, buy_price, amt

        if iscrypto:
            current_profit_percent = (cur_price - buy_price) / cur_price
            
            #if current_profit_percent - 0.015 > max_profit_percent:
            #    max_profit_percent = current_profit_percent - 0.015

            if current_profit_percent > 0:
                if current_profit_percent < max_profit_percent and not boughtcandle:
                    iscrypto = False
                    amt = amt * cur_price
                    print('/ / / / / / / / / sold @ ', cur_price, '\n', amt)
                    soldcandle = True

                elif avg25[-1] > last25[-1] or (cur_price - buy_price) / 100 < -0.03 and not boughtcandle:
                    iscrypto = False
                    amt = amt * cur_price
                    print('/ / / / / / / / / sold @ ', cur_price, '\n', amt)
                    soldcandle = True

        else: 
            if last25[-1] > avg25[-1] and last25[-2] > avg25[-2] and last25[-3] <= avg25[-3] and last25[-1] >= last25[-2] and last25[-2] >= last25[-3] and not soldcandle:
                iscrypto = True
                amt = amt / cur_price
                buy_price = cur_price
                max_profit_percent = -0.02
                print('+ + + + + + + + + bought @ ', buy_price)
                boughtcandle = True
    """

    #response = client.get_open_orders(coin.upper())
    #print(response)



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

coin = 'ETHUSDT'

socket = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

ws = websocket.WebSocketApp(socket, on_open = wsopen, on_close = wsclose, on_message = wsmsg)

testnet = True
timeclient = CL()
#print(client.time())
#print([testkey, testsecret])
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
        print(timeclient.time())

    elif whattodo == 'start':
        last25 = []
        avg25 = []
        iscrypto = False
        max_profit_percent = 0
        cur_price = 0
        rsi = []
        posdiff = []
        negdiff = []
        ws.run_forever()
        vassets = open("vassets.txt", "w")
        if iscrypto:
            amt = amt * cur_price
            iscrypto = False
        print(amt, file = vassets)
        vassets.close()
        

    elif whattodo == 'exit' or whattodo == 'quit' or whattodo == 'q':
        break

    elif whattodo == 'crypto' or whattodo == 'cr' or whattodo == 'cc':
        coin = input('Type your crypto pair: ').upper().strip()
        socket = 'wss://stream.binance.com:9443/ws/'+ coin.lower() +'@kline_1m'
        ws = websocket.WebSocketApp(socket, on_open = wsopen, on_close = wsclose, on_message = wsmsg)

    elif whattodo == 'yo':
        print('\nyo')
    
    elif whattodo == 'amt':
        print('\n', amt)

    else:
        print('\nwhat\n')


print('')

stop = time.time()
sec = math.trunc(stop - start)
if(sec > 1):
    hr = sec // 3600
    mn = sec // 60 % 60
    sec = sec % 60
    if hr:
        print('bot ran for ', hr, 'h ', mn, 'm ', sec, 's', sep = '')
    elif mn:
        print('bot ran for ', mn, 'm ', sec, 's', sep = '')
    else:
        print('bot ran for ', sec, 's', sep = '')

print('cya')