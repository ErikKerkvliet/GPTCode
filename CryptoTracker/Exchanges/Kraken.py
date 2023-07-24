from time import sleep

import keys
import globalvar
import requests

from CostHandler import CostHandler
from packages.kraken.exceptions import KrakenException
from packages.kraken.base_api import KrakenBaseSpotAPI, defined, ensure_string
from packages.kraken.spot import Trade
from packages.kraken.spot import User


class Kraken:
    def __init__(self, glv):
        self.glv = glv
        self.client = None
        self.user = None
        self.times = 0
        self.pairs = self.asset_pairs()
        self.cost_handler = CostHandler()

    def get_user(self) -> User:
        if self.user is not None:
            return self.user
        self.user = User(key=keys.KEY_KRAKEN_API, secret=keys.KEY_KRAKEN_PRIVATE)
        return self.user

    def get_client(self) -> Trade:
        if self.client is not None:
            return self.client
        self.client = Trade(key=keys.KEY_KRAKEN_API, secret=keys.KEY_KRAKEN_PRIVATE)
        return self.client

    def close_client(self):
        if not self.client:
            return

        self.client.close()
        self.client = None

    def buy(self, crypto, amount=None):
        if not amount:
            amount = crypto.amount

        order_data = {
            'ordertype': 'market',
            'side': 'buy',
            'pair': crypto.pair,
            'amount': amount,
            'crypto': crypto,
            'validate': True,  # Test variable
        }

        if not globalvar.TEST:
            order_data['validate'] = False

        self.create_order(order_data)

        self.cost_handler.buy(crypto)

    def sell(self, crypto, amount=None):
        if not amount:
            amount = crypto.amount

        order_data = {
            'ordertype': 'market',
            'side': 'sell',
            'pair': crypto.pair,
            'amount': amount,
            'crypto': crypto,
            'validate': True,  # Test variable
        }

        if not globalvar.TEST:
            order_data['validate'] = False

        self.create_order(order_data)

        self.cost_handler.sell(crypto)

    def get_balances(self):
        with self.get_user() as user:
            balances = user.get_balances()

        cryptos = {}
        for key in balances.keys():
            if key == 'ZEUR':
                continue
            cryptos[key] = balances[key]['balance']
        return cryptos

    def get_balance_euro(self):
        with self.get_user() as user:
            euro_balance = user.get_balance('EUR')['available_balance']
        return euro_balance


    def create_order(self, order_data):

        print(f'{self.glv.tracker} {order_data["side"]} | {order_data["crypto"].pair}: {order_data["amount"]}')
        return
        self.get_client().create_order(
            ordertype=order_data['ordertype'],
            side=order_data['side'],
            pair=order_data['pair'],
            volume=order_data['amount'],
            validate=order_data['validate']
        )

    def asset_pairs(self, crypto_code=None):
        url = f'https://api.kraken.com/0/public/AssetPairs'
        if crypto_code:
            url += f'?pair={crypto_code}EUR'
        response = requests.get(url)

        response_data = response.json()
        response.close()

        if response_data['error'] and self.times < 3:
            sleep(5)
            self.asset_pairs()
        self.times = 0

        crypto_data = response_data['result']
        cryptos = {}
        for code in crypto_data.keys():
            if code[-3:] == 'EUR' and crypto_data[code]['status'] == 'online':
                cryptos[code] = crypto_data[code]
        return cryptos

    def ticker(self, crypto_code=None, wallet=None) -> dict:
        url = f'https://api.kraken.com/0/public/Ticker'
        if crypto_code:
            url += f'?pair={crypto_code}EUR'
        response = requests.get(url)

        response_data = response.json()
        response.close()

        if response_data['error'] and self.times < 3:
            self.times += 1
            sleep(5)
            self.ticker()
        self.times = 0

        crypto_data = response_data['result']
        for code in crypto_data.keys():
            if code[-3:] == 'EUR' and code in self.pairs.keys() and self.pairs[code]['status'] == 'online':
                currency_code = code.replace('EUR', '')
                if currency_code in wallet.keys():
                    wallet[currency_code].set_rate(crypto_data[code]['c'][0])
                    wallet[currency_code].pair = self.pairs[code]['wsname']
                    wallet[currency_code].trade_amount_min = self.pairs[code]['ordermin']
        return wallet
