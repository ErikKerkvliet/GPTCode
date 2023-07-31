import json
import keys
import math
from time import sleep

import globalvar
from CostHandler import CostHandler

from packages.bitpanda.BitpandaClient import BitpandaClient
from packages.bitpanda.enums import OrderSide
from packages.bitpanda.Pair import Pair
from Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client
import requests

import tracemalloc
import asyncio


class Bitpanda:

    def __init__(self, glv):
        self.glv = glv
        self.client = None
        tracemalloc.start()
        self.times = 0
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

    def ticker(self, crypto_code='ALL', wallet=None) -> dict:
        if wallet is None:
            wallet = {}
        url = 'http://api.bitpanda.com/v1/ticker'
        response = requests.get(url)

        response_data = response.json()
        response.close()

        cryptos = {}
        for code in response_data.keys():
            if code != globalvar.DEFAULT_CURRENCY:
                cryptos[code] = response_data[code]

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_account_balances())

        crypto_data = {}
        for crypto in response['response']['balances']:
            if crypto['currency_code'] != globalvar.DEFAULT_CURRENCY:
                crypto_data[crypto['currency_code']] = crypto

        for code in crypto_data.keys():
            if code in self.pairs.keys() \
                    and self.pairs[code]['state'] == 'ACTIVE' \
                    and code in wallet.keys():
                wallet[code].pair = f'{code}_EUR'
                wallet[code].set_rate(cryptos[code][globalvar.DEFAULT_CURRENCY])
                wallet[code].trade_amount_min = float(self.pairs[code]['min_size'])

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

        amount = math.floor(amount * float(f'1e{precision}')) / float(f'1e{precision}')
        order_data = {
            'pair': f'{crypto.code}_{globalvar.DEFAULT_CURRENCY}',
            'exchange_type': side,
            'amount': float(f'{float(amount):.{precision}f}'),
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

    def asset_pairs(self, code='ALL'):
        if self.instruments:
            if code and code != 'ALL':
                return self.instruments[code]
            else:
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
        number = (order_data['crypto'].amount / order_data['crypto'].rate) if order_data["exchange_type"] == 'SELL' else \
            globalvar.BUY_AMOUNT * float(((order_data['crypto'].rate / order_data['crypto'].buy_rate * 100 + 1) / 100))
        amount_euro = f"{float(number):.8f}"
        print(f'Bitpanda {order_data["exchange_type"]}, Pair: {order_data["pair"]}, Amount: {order_data["amount"]}, Amount €: {amount_euro}')
        return
        #
        # if globalvar.STATE is globalvar.STATE_PRODUCTION:
        #     print('NOOOOO !!!!!!!!!!!!!!!!!!!')
        #     exit()

        # headers = {
        #     'Content-Type': 'application/json',
        #     'Accept': 'application/json',
        #     'Authorization': "Bearer " + keys.KEY_TRADE
        # }
        #
        # data = {
        #     "instrument_code": "SHIB_EUR",
        #     "side": "BUY",
        #     "type": "MARKET",
        #     "amount": "1984126"
        # }
        # data = json.dumps(data)
        # r = requests.post('https://api.exchange.bitpanda.com/public/v1/account/orders', headers=headers, data=data)
        #
        # return r.json()

        return await self.get_client().create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        )

    @staticmethod
    def get_balance_euro() -> float:
        return 0.0
