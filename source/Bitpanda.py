import json
import keys

import source.globalvar as globalvar

from packages.bitpanda.BitpandaClient import BitpandaClient
from source.Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
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

    @staticmethod
    def get_client():
        if globalvar.get_ip() == globalvar.IP_WORK:
            return BitpandaClient(keys.KEY_NON_PRO)
        else:
            return BitpandaClient(keys.KEY_TRADE)

    async def close_client(self):
        if not self.client:
            return

        await self.client.close()
        self.client = None

    def ticker(self, coin='ALL', currency='ALL'):
        data = None
        crypto_codes = []
        if not self.client:
            self.client = self.get_client()

        if globalvar.get_ip() == globalvar.IP_HOME:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(self.client.get_currencies())

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
        amount = crypto.amount

        if globalvar.get_ip() == globalvar.IP_HOME:
            precision = crypto.instrument['amount_precision']
            trade_amount = round(amount, precision)
        else:
            trade_amount = round(amount, 5)

        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.SELL,
            'amount': trade_amount,
            'crypto': crypto,
        }
        if self.client is None:
            self.client = self.get_client()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_order(order_data))

        crypto.profit += (crypto.rate - crypto.buy_rate)
        crypto.profit_euro += ((crypto.rate - crypto.buy_rate) / crypto.rate)

        crypto.amount -= amount
        crypto.amount_euro = crypto.amount / crypto.rate

        crypto.sells += 1
        crypto.position = 0
        crypto.more = 0
        crypto.less = 0

    def buy(self, crypto, amount=None):
        rate = self.ticker(crypto.code, globalvar.DEFAULT_CURRENCY)

        if not amount:
            amount = crypto.amount

        if self.client is None:
            self.client = self.get_client()

        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCY)

        if globalvar.get_ip() == globalvar.IP_HOME:
            precision = crypto.instrument['amount_precision']
            trade_amount = round(amount, precision)
        else:
            trade_amount = round(amount, 5)

        # BTC_EURO
        # + 0.00039 BTC
        # - 10 EUR
        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.BUY,
            'amount': trade_amount,
            'crypto': crypto,
        }

        if self.client is None:
            self.client = self.get_client()

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.create_order(order_data))

        self.client.close()

        crypto.buy_rate = crypto.rate
        crypto.amount += amount * 11
        crypto.amount_euro += crypto.amount / crypto.rate

        self.response['rate'] = float(rate)
        self.response['amount_euro'] = crypto.amount / crypto.rate

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
        amount = f'{float(order_data["amount"]):.8f}'
        amount_euro = f"{(float(order_data['crypto'].amount) / float(order_data['crypto'].rate)):.8f}"
        print(f'Type: {order_data["exchange_type"]}, Pair: {order_data["pair"]}, Amount: {amount}, Amount €: {amount_euro}')

        if globalvar.STATE == globalvar.STATE_DEVELOPMENT or globalvar.get_ip() == globalvar.IP_WORK:
            self.response = {
                'code': order_data['pair'],
                'amount': order_data['amount'],
            }
            return self.response
        #
        # if globalvar.STATE is globalvar.STATE_PRODUCTION:
        #     print('NOOOOO !!!!!!!!!!!!!!!!!!!')
        #     exit()
        return await self.client.create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        )
