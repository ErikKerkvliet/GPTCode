import keys
import math

import globalvar
from CostHandler import CostHandler
from Crypto import Crypto

from packages.bitpanda.BitpandaClient import BitpandaClient
from packages.bitpanda.enums import OrderSide
import requests

import tracemalloc
import asyncio


class Bitpanda:

    def __init__(self, glv):
        self.glv = glv
        self.client = None
        tracemalloc.start()
        self.times = 0
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

    def ticker(self, wallet: dict) -> dict:
        url = 'http://api.bitpanda.com/v1/ticker'
        response = requests.get(url)

        response_data = response.json()
        response.close()

        for code in response_data.keys():
            if code in wallet.keys():
                wallet[code].set_rate(response_data[code][globalvar.DEFAULT_CURRENCY])
        return wallet

    def get_balances(self, wallet: dict):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_account_balances())
        balances = response['response']['balances']

        for balance in balances:
            code = balance['currency_code']
            if code not in wallet.keys():
                wallet[code] = Crypto(code)
            wallet[code].balance = float(balance['available'])
        return wallet

    def start_transaction(self, crypto, side):
        if crypto.code == globalvar.DEFAULT_CURRENCY:
            return

        precision = crypto.pair['pair_decimals']

        if side == globalvar.ORDER_SIDE_BUY:
            amount = crypto.buy_amount_euro / crypto.rate
            side = OrderSide.BUY
        else:
            amount = crypto.balance
            side = OrderSide.SELL

        amount = math.floor(amount * float(f'1e{precision}')) / float(f'1e{precision}')
        order_data = {
            'pair': f'{crypto.code}_{globalvar.DEFAULT_CURRENCY}',
            'exchange_type': side,
            'amount': f'{float(amount):.{precision}f}',
            'crypto': crypto,
        }

        response = self.create_order(order_data)

        print(response)

        if side == OrderSide.BUY:
            self.cost_handler.buy(crypto)
        else:
            self.cost_handler.sell(crypto)

    def fill_assets(self, wallet: dict) -> dict:
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_instruments())
        response_data = response['response']
        for asset in response_data:
            code = asset['base']['code']
            if code in wallet.keys():
                wallet[code].asset = asset
                wallet[code].trade_amount_min = float(asset['min_size'])
        return self.pairs(wallet)

    def pairs(self, wallet: dict) -> dict:
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_instruments())
        response_data = response['response']
        # self.client.close()

        for pair in response_data:
            if pair['base']['code'] in wallet.keys() and pair['state'] == 'ACTIVE':
                wallet[pair['base']['code']].pair = wallet
        return wallet

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    def create_order(self, order_data) -> dict:
        print(f'=============== Bitpanda {order_data["exchange_type"]} | Euro: {order_data["amount"] / order_data["crypto"].rate} ===============')
        print(order_data["exchange_type"])

        if globalvar.TEST:
            return {}

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.get_client().create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        ))
