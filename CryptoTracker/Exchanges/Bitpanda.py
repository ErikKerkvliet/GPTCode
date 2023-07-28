import json
import keys
import math

import globalvar
from CostHandler import CostHandler

from packages.bitpanda.BitpandaClient import BitpandaClient
from packages.bitpanda.enums import OrderSide
from packages.bitpanda.Pair import Pair
from Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client

import tracemalloc
import asyncio


class Bitpanda:

    def __init__(self, glv):
        self.glv = glv
        self.client = None
        tracemalloc.start()
        self.instruments = {}
        self.response = {}
        self.cost_handler = CostHandler()

    def get_client(self):
        if self.client is not None:
            return self.client

        # if self.glv.ip == globalvar.IP_WORK:
        #     self.client = BitpandaClient(keys.KEY_NON_PRO)
        # else:
        self.client = BitpandaClient(keys.KEY_TRADE)
        return self.client

    def close_client(self):
        if not self.client:
            return

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.client.close())
        self.client = None

    def ticker(self, coin='ALL') -> dict:
        data = None
        crypto_codes = []

        if self.glv.ip == globalvar.IP_HOME:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(self.get_client().get_account_balances())
            response_data = response['response']['balances']

            for crypto in response_data:
                crypto_codes.append(crypto['currency_code'])

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

        wallet = {}
        if not crypto_codes:
            for crypto in response_data.keys():
                wallet[crypto] = response_data[crypto][globalvar.DEFAULT_CURRENCY]
        else:
            for crypto in response_data.keys():
                if crypto in crypto_codes:
                    wallet[crypto] = response_data[crypto][globalvar.DEFAULT_CURRENCY]
        if coin != 'ALL' and coin not in wallet.keys():
            raise CoinIndexNotFoundException

        if coin == 'ALL':
            coins_data = {}
            for coin in wallet.keys():
                coins_data[coin] = float(wallet[coin])
            return coins_data

        if coin == 'ALL':
            return wallet
        return wallet

    async def get_balances(self, coin='all'):
        response = await self.get_client().get_account_balances()

        if coin == 'all':
            return response['response']['balances']
        return response['response']['balances'][coin]

    def start_transaction(self, crypto, side):
        if crypto.code == 'BTC':
            return

        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCY)

        # - 0.00036 BTC
        # + 10.02 EUR
        precision = crypto.instrument['amount_precision']

        if side == globalvar.ORDER_SIDE_BUY:
            amount = crypto.buy_amount_euro / crypto.rate
            side = OrderSide.BUY
        else:
            amount = crypto.amount
            side = OrderSide.SELL

        order_data = {
            'pair': pair,
            'exchange_type': side,
            'amount': math.floor(amount * float(f'1e{precision}')) / float(f'1e{precision}'),
            'crypto': crypto,
        }

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.create_order(order_data))

        # self.client.close()

        print(response)
        if side == OrderSide.BUY:
            self.cost_handler.buy(crypto)
        else:
            self.cost_handler.sell(crypto)

    def get_instrument(self, code='ALL'):
        if self.instruments:
            return self.instruments

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_instruments())

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

        if code == 'ALL':
            return self.instruments

        return self.instruments[code]

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    async def create_order(self, order_data) -> dict:
        amount = f'{float(order_data["amount"]):.8f}'

        number = (order_data['crypto'].amount / order_data['crypto'].rate) if order_data["exchange_type"] == 'SELL' else \
            globalvar.BUY_AMOUNT * float(((order_data['crypto'].rate / order_data['crypto'].buy_rate * 100 + 1) / 100))
        amount_euro = f"{float(number):.8f}"
        print(f'Bitpanda {order_data["exchange_type"]}, Pair: {order_data["pair"]}, Amount: {amount}, Amount €: {amount_euro}')
        return
        # if globalvar.STATE == globalvar.STATE_DEVELOPMENT or self.glv.ip == globalvar.IP_WORK:
        #     self.response = {
        #         'code': order_data['pair'],
        #         'amount': order_data['amount'],
        #     }
        #     return self.response

        # print(order_data)
        # return

        #
        # if globalvar.STATE is globalvar.STATE_PRODUCTION:
        #     print('NOOOOO !!!!!!!!!!!!!!!!!!!')
        #     exit()
        return await self.get_client().create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        )
