vicki_contr = 714
abe_contr = ((105000 * 0.09) / 26) + 1000

vicki_amount = 69000.0
abe_amount = 17000.0

# print (vicki_amount / (abe_contr - vicki_contr)) / 26

# init + (rate * t) = myinit + (myrate * t)
# init + (rate * t) - (myrate * t) = myinit
# (rate * t) - (myrate * t) = myinit - init
# t * (rate - myrate) = myinit - init



# def calc_time(init, rate, myinit, myrate):
#     return (myinit - init) / (rate - myrate)

# def calc_time2(init, rate, myinit, myrate):
#     return (init - myinit) / (myrate - rate)


# year_time = (calc_time(vicki_amount, vicki_contr, abe_amount, abe_contr))
# year_time2 = (calc_time2(vicki_amount, vicki_contr, abe_amount, abe_contr))
# print year_time == year_time2
# print year_time / 26
# print (abe_amount + (abe_contr * year_time))
# print (vicki_amount + (vicki_contr * year_time))

# print 1174.57751923 - 330.62654272
# print 6.42436025 - 1.75279386

# init_price = 3600.00
# quantity = 0.49
# with open('/tmp/BCC.csv') as _file:
#     for line in _file:
#         vals = line.strip('\n').split(',')
#         if len(vals) < 3:
#             continue

#         gain = float(vals[1]) / init_price
#         print '%s: %s' % (vals[0], (gain - 1) * 100)


# vals = [400.0, 400, 400, 250, 370]
# avg_gain = sum(vals) / len(vals)
# print (2000 * (avg_gain / 100)) + 2000




init_price = 3300.0
# print ((3400 - init_price) / init_price) * 100
# print ((5000 - init_price) / init_price) * 100
# print ((7000 - init_price) / init_price) * 100
# print ((10000 - init_price) / init_price) * 100
# print ((15000 - init_price) / init_price) * 100
# print ((20000 - init_price) / init_price) * 100
# print ((25000 - init_price) / init_price) * 100

btc_prices = [
    3400,
    5000,
    7000,
    10000,
    15000,
    20000,
    25000,
]
ltc_prices = [
    78,
    88,
    112,
    150,
    200,
    250,
    350,
]
btc_q = 0.15044
ltc_q = 1.75 * 2

values = [0] * 8
# for idx, p in enumerate(btc_prices):
#     print btc_q * p
#     values[idx] += (btc_q * p)

# for idx, p in enumerate(ltc_prices):
#     print ltc_q * p
#     values[idx] += (ltc_q * p)

# print
# values[7] += (btc_q / 2) * btc_prices[-1]
# values[7] += (ltc_q / 2) * ltc_prices[-1]

# for v in values:
#     print v


# btc_pp = 3300.0
# ltc_pp = 75
# for idx, p in enumerate(btc_prices):
#     val = ((p - btc_pp) / btc_pp) * 100
#     print val
#     values[idx] += val

# for idx, p in enumerate(ltc_prices):
#     val = ((p - ltc_pp) / ltc_pp) * 100
#     print val
#     values[idx] += val

# print
# values[7] += ((btc_prices[-1] - btc_pp) / btc_pp) * 100
# values[7] += ((ltc_prices[-1] - ltc_pp) / ltc_pp) * 100

# for v in values:
#     print v / 2
# DOGE,47390.53200,0.0075,354.04,-21.28
string = """ADA,84.00,1.26,106.09,-16.04
DASH,0.36,1464.72,533.13,287.73
DOGE,47390.53,0.0204,965.49,114.45
ETH,1.35,1309.24,1765.77,367.88
LTC,1.75,359.73,630.52,494.83
NEO,2.00,124.47,248.94,-6.85
XLM,1289.21,0.92,1188.45,15.33
XRP,1174.58,3.3754,3964.73,477.40
XVG,570.27,0.22,127.19,1.14"""

# total = 0
# for v in string.split('\n'):
#     vals = v.split(',')
#     total += float(vals[3])

# print total
# print 248.94 / 2
# wavg = []
# avg = []
# for v in string.split('\n'):
#     vals = v.split(',')
#     weight = float(vals[3]) / total
#     pgain = float(vals[4]) * weight
#     print '%s: %s (%s)' % (vals[0], pgain, vals[4])
#     wavg.append(pgain)
#     avg.append(float(vals[4]))

# print 'weighted avg gain: %.2f' % sum(wavg)
# print 'avg gain: %.2f' % (sum(avg) / len(avg))




# eth1_shares = 1.75506972
# eth1_price = 465.00 / eth1_shares

# eth2_shares = 0.94231685
# eth2_pprice = 289.80 / eth2_shares
# print eth1_price
# print eth2_pprice
# num_shares = (1.75506972 + 0.94231685)
# print ((eth1_price * eth1_shares) + (eth2_pprice * eth2_shares)) / num_shares

# # 4cc53bba-76ff
# ltc_shares = 3.50558771
# ltc_pprice = 212.0 / ltc_shares
# print ltc_pprice

# # e5beaec1-852c
# dash_shares = 0.72795723
# dash_pprice = 275.0 / dash_shares
# print dash_pprice

# print 47390.53200 * 0.0075


# btc_cad = 5747
# btc_usd = 7899
# btc_ltc = 1949700
# btc_bhc = 20338500
# satoshi = 100000000.0

# prices = [
#     btc_usd,
#     btc_ltc,
#     btc_bhc,
# ]
# cad_price = satoshi / btc_cad
# for p in prices:
#     val = satoshi / p
#     print cad_price / val

# kw_hours = 1 * 24
# kwh_per_month = kw_hours * 30

# kwh_cost = 0.1243

# cost_per_month = kwh_per_month * kwh_cost
# print kwh_per_month
# print cost_per_month

# print 2.54504300 - 1.34869329


# a = 0.00068981 * 1135.05
# b = 0.00070838 * 1135.05

# total = 1289.21007234
# print ((b * 1000) + (a * (total - 1000))) / total
# print 0.42000000 * 1135.05
# print 0.415 * 1135.05
# cad_price = 1.2515

# verge_quantity = 570.27330268
# verge_pprice_us = 0.17619999
# verge_spent_us = 100.73336131
# print verge_pprice_us * cad_price


# ada_quantity = 84.00000000
# ada_pprice_us = 1.20201600 
# ada_spent_us = 101.22176815
# print ada_pprice_us * cad_price

# neo_quantity = 2.00000000
# neo_pprice_us = 106.76809945
# neo_spent_us = 214.07003939
# print neo_quantity * neo_pprice_us
# print neo_pprice_us * cad_price


# fuel_cost = 6.00  # per gallon
# gallons_per_hour = 17

# cost_per_hour = fuel_cost * gallons_per_hour
# print cost_per_hour

# key = 'x3JJHMbDL1EzLkh9GBhXDw=='
# import hashlib
# import base64
# resp = 'HSmrc0sMlYUkAGmm5OPpG2HaGWk='
# append = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
# hasher = hashlib.sha1()
# hasher.update(key + append)
# assert base64.b64encode(hasher.digest()) == resp
# print base64.b64encode(hasher.digest())

vals = [
    1842.3499,
    1838.0900,
    1774.8952,
    1899.6431,
    2182.5310,
    1936.7899,
    1972.4126,
    1985.0010,
    1957.6803,
    2060.6863,
    2318.9257,
    2308.8230,
    2289.9095,
    2230.2141,
    2221.7935,
    2134.5773,
    2175.1262,
    2025.9958,
    1958.1500,
    1953.6594,
    1825.0554,
    1769.4668,
    1256.3791,
    1257.6256,
    1254.5618,
    1279.2454,
    1280.1953,
    1292.1076,
    1306.3169,
    1297.7291,
    1278.9723,
    1108.5066,
]

def derivative(x, xdelta, y, ydelta):
    return (ydelta - y) / (xdelta - x)


# for idx in xrange(1, len(vals) - 1):
#     x = idx - 1
#     xdelta = idx + 1
#     y = vals[x]
#     ydelta = vals[xdelta]
#     thing = derivative(x, xdelta, y, ydelta)
#     print thing

import json
import requests

def _get(addr):
    """generic wrapper around requests.get"""
    resp = requests.get(addr)
    if resp.status_code != 200:
        raise Exception('rc from %s: %s' % (addr, resp.status_code))

    content = resp.content
    if isinstance(content, bytes):
        return content.decode('utf-8')

    return content


def _get_bittrex(addr):
    """wrapper around requests.get that prints error message on non 200
    HTTP resp code for requests to the Bittrex API"""
    data = json.loads(_get(addr))
    assert data['success'], 'unsuccesful resp: (%s) %s' % (addr, data['message'])
    return data['result']

BITTREX_API = 'https://bittrex.com/api/v1.1/public/'

def get_order_book(market):
    addr = BITTREX_API + 'getorderbook?market=%s&type=both' % market
    return  _get_bittrex(addr)

def _spread(bid, ask):
    return (ask - bid) / ask

def print_diff(data):
    selldata = data['sell']
    buydata = data['buy']

    selllow = selldata[0]['Rate']
    sellhigh = selldata[-1]['Rate']

    buylow = buydata[-1]['Rate']
    buyhigh = buydata[0]['Rate']

    selldiff = sellhigh - selllow
    buydiff = buyhigh - buylow

    spread = _spread(buyhigh, selllow)
    print spread * 100
    # print buyhigh
    # print selllow
    # print '~~~~~~'
    # print selldiff
    # print buydiff
    # print '=========='

# with open('/tmp/usdt-xrp.orders') as _file:
#     data = json.loads(_file.read())
#     print_diff(data)
#     print_diff(get_order_book('USDT-XRP'))

# results = _get_bittrex(BITTREX_API + 'getmarkethistory?market=BTC-XRP')

# buys = []
# sells = []
# for v in results:
#     if v['FillType'] == 'PARTIAL_FILL':
#         continue
#     print v
#     if v['OrderType'] == 'BUY':
#         buys.append(v['Price'])
#     else:
#         sells.append(v['Price'])

# print buys
# print
# print sells