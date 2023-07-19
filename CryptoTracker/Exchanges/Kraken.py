from time import sleep

import keys
import globalvar
import requests

from packages.kraken.exceptions import KrakenException
from packages.kraken.base_api import KrakenBaseSpotAPI, defined, ensure_string
from packages.kraken.spot import Trade
from packages.kraken.spot import User


class Kraken:
    def __init__(self, glv):
        self.glv = glv
        self.client = None
        self.user = User(key=keys.KEY_KRAKEN_API, secret=keys.KEY_KRAKEN_PRIVATE)
        self.times = 0
        self.pairs = self.asset_pairs()

    def get_client(self):
        if self.client is not None:
            return self.client
        return KrakenBaseSpotAPI(key=keys.KEY_KRAKEN_API)

    async def close_client(self):
        if not self.client:
            return

        await self.client.close()
        self.client = None

    async def buy(self, crypto):

        order_data = {
            'ordertype': 'market',
            'side': 'buy',
            'pair': '',
            'amount': crypto.amount,
            'validate': True  # Test variable
        }

        if not globalvar.TEST:
            order_data['validate'] = False

        await self.create_order(order_data)

    def sell(self, crypto):
        pass

    def get_balances(self):
        with self.user as user:
            balances = user.get_balances()

        cryptos = {}
        for key in balances.keys():
            cryptos[key] = balances[key]['balance']
        return cryptos

    async def create_order(self, order_data):

        self.client.create_order(
            ordertype=order_data,
            side=order_data,
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

    def ticker(self, crypto_code=None) -> dict:
        url = f'https://api.kraken.com/0/public/Ticker'
        if crypto_code:
            url += f'?pair={crypto_code}EUR'
        response = requests.get(url)

        response_data = response.json()

        if response_data['error'] and self.times < 3:
            self.times += 1
            sleep(5)
            self.ticker()
        self.times = 0

        crypto_data = response_data['result']
        cryptos = {}
        for code in crypto_data.keys():
            if code[-3:] == 'EUR' and code in self.pairs.keys() and self.pairs[code]['status'] == 'online':
                cryptos[code] = crypto_data[code]['c'][0]
        return cryptos
