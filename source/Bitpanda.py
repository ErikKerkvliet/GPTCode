import json
import keys

import globalvar

from bitpanda.BitpandaClient import BitpandaClient, MarketTickerSubscription
from Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client
from bitpanda.enums import OrderSide
from bitpanda.Pair import Pair
import asyncio
import requests


class Bitpanda:

    def __init__(self):
        if globalvar.get_ip() == globalvar.IP_WORK:
            self.client = BitpandaClient(keys.KEY_NON_PRO)
        else:
            self.client = BitpandaClient(keys.KEY_TRADE)

        self.instruments = {}
        self.response = {}

    @staticmethod
    def ticker(coin='ALL', currency='ALL'):
        data = None

        connection = http.client.HTTPSConnection("api.bitpanda.com")
        while data is None:
            try:
                headers = {'Accept': "application/json"}

                connection.request("GET", "/v1/ticker", headers=headers)

                response = connection.getresponse()
                data = response.read()
            except http.client.NotConnected:
                print('Exception: disconnected. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue
            except http.client.HTTPException:
                print('Exception: HTTP Exception. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue

        response_data = json.loads(data.decode("utf-8"))

        if coin != 'ALL' and coin not in response_data.keys():
            raise CoinIndexNotFoundException

        if coin == 'ALL' and currency != 'ALL':
            coins_data = {}
            for coin in response_data.keys():
                coins_data[coin] = {}
                for currency_code in response_data[coin].keys():
                    coins_data[coin] = float(response_data[coin][currency_code])
            return coins_data

        if coin == 'ALL':
            return response_data

        if currency not in response_data[coin]:
            raise CurrencyIndexNotFoundException

        if currency == 'ALL':
            return response_data[coin]

        return float(response_data[coin][currency])

    async def get_balances(self, coin='all'):
        response = await self.client.get_account_balances()
        await self.client.close()

        if coin == 'all':
            return response['response']['balances']
        return response['response']['balances'][coin]

    def sell(self, crypto):
        pair = Pair('BTC', globalvar.DEFAULT_CURRENCY)

        # - 0.00036 BTC
        # + 10.02 EUR
        amount = crypto.amount / crypto.rate
        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.SELL,
            'amount': crypto.amount,
        }
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_order(order_data))
        crypto.profit += crypto.last_rate - (crypto.buy_rate * globalvar.SELL_PERC)
        crypto.sells += 1
        crypto.position = 0
        crypto.more = 0
        crypto.less = 0
        # self.client.close()

    def buy(self, crypto, amount=None):
        rate = self.ticker(crypto.code, globalvar.DEFAULT_CURRENCY)

        if not amount:
            amount = globalvar.BUY_AMOUNT / crypto.rate

        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCY)
        instruments = self.get_instrument()
        if crypto.code not in globalvar.DEFAULT_CURRENCY \
                or instruments[crypto.code]['state'] != 'ACTIVE' \
                or amount < instruments[crypto.code]['min_size']:
            return False

        amount = float(10)
        precision = instruments[crypto.code]['amount_precision']
        amount = f'{amount:.{precision}f}'

        # + 2451378 SHIB
        # - 10 EUR
        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.BUY,
            # 'amount': '2451378',
        }

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.create_order(order_data))
        self.client.close()

        crypto.buy_rate = crypto.rate
        crypto.amount = crypto.rate * 10

        self.response['rate'] = float(rate)
        self.response['amount_euro'] = globalvar.BUY_AMOUNT

        return self.response

    def get_instrument(self, crypto='ALL'):
        if self.instruments:
            return self.instruments

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.client.get_instruments())
        # self.client.close()

        for instrument in response['response']:
            self.instruments[instrument['base']['code']] = {
                'state': instrument['state'],
                'code': instrument['base']['code'],
                'precision': int(instrument['base']['precision']),
                'amount_precision': int(instrument['amount_precision']),
                'market_precision': int(instrument['market_precision']),
                'min_size': float(instrument['min_size']),
            }
            # print(self.instruments[instrument['base']['code']])

        if crypto == 'ALL':
            return self.instruments

        return self.instruments[crypto]

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    async def create_order(self, order_data) -> dict:
        print(f'Type: {order_data["exchange_type"]}, Pair: {order_data["pair"]}, Amount: {order_data["amount"]}')
        if globalvar.TEST or globalvar.get_ip() == globalvar.IP_WORK:
            self.response = {
                'code': order_data['pair'],
                'amount': order_data['amount'],
            }
            return self.response

        # return await self.client.create_market_order(
        #     order_data['pair'],
        #     order_data['exchange_type'],
        #     order_data['amount']
        # )
