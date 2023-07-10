import json
import keys

import globalvar

from packages.bitpanda.BitpandaClient import BitpandaClient
from Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client
from packages.bitpanda.enums import OrderSide
from packages.bitpanda.Pair import Pair
import asyncio
import requests


class Bitpanda:

    def __init__(self):
        self.client = self.get_client()

        self.instruments = {}
        self.response = {}

    def get_client(self):
        if globalvar.get_ip() == globalvar.IP_WORK:
            return BitpandaClient(keys.KEY_NON_PRO)
        else:
            return BitpandaClient(keys.KEY_TRADE)

    async def close_client(self):
        await self.client.close()

    def ticker(self, coin='ALL', currency='ALL'):
        data = None
        crypto_codes = []
        if not self.client:
            self.client = self.get_client()

        if globalvar.get_ip() == globalvar.IP_HOME:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(self.client.get_currencies())
            self.close_client()

            for crypto in response['response']:
                crypto_codes.append(crypto['code'])
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

        if not crypto_codes:
            wallet = response_data
        else:
            wallet = {}
            for crypto in response_data.keys():
                if crypto in crypto_codes:
                    wallet[crypto] = response_data[crypto]

        if coin != 'ALL' and coin not in wallet.keys():
            raise CoinIndexNotFoundException

        if coin == 'ALL' and currency != 'ALL':
            coins_data = {}
            for coin in wallet.keys():
                coins_data[coin] = {}
                for currency_code in wallet[coin].keys():
                    coins_data[coin] = float(wallet[coin][currency_code])
            return coins_data

        if coin == 'ALL':
            return wallet

        if currency not in wallet[coin]:
            raise CurrencyIndexNotFoundException

        if currency == 'ALL':
            return wallet[coin]

        return float(wallet[coin][currency])

    async def get_balances(self, coin='all'):
        response = await self.client.get_account_balances()

        if coin == 'all':
            return response['response']['balances']
        return response['response']['balances'][coin]

    def sell(self, crypto):
        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCY)

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
        crypto.profit_euro += crypto.profit / crypto.rate
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
        # print(sorted(list(self.instruments)))

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

        if globalvar.STATE == globalvar.STATE_DEVELOPMENT or globalvar.get_ip() == globalvar.IP_WORK:
            self.response = {
                'code': order_data['pair'],
                'amount': order_data['amount'],
            }
            return self.response

        if globalvar.STATE is globalvar.STATE_PRODUCTION:
            print('NOOOOO !!!!!!!!!!!!!!!!!!!')
            exit()
            return await self.client.create_market_order(
                order_data['pair'],
                order_data['exchange_type'],
                order_data['amount']
            )
