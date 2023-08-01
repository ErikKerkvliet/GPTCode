from time import sleep

import keys
import globalvar
import requests

from CostHandler import CostHandler
from Crypto import Crypto
from packages.kraken.spot import Trade
from packages.kraken.spot import User


class Kraken:
    def __init__(self, glv):
        self.glv = glv
        self.client = None
        self.user = None
        self.times = 0
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

    def start_transaction(self, crypto, side):
        crypto.pair = f'{crypto.code}/{globalvar.DEFAULT_CURRENCY}'
        if side == globalvar.ORDER_SIDE_BUY:
            amount = crypto.buy_amount_euro / crypto.rate
            side = globalvar.ORDER_SIDE_BUY
        else:
            amount = crypto.amount
            side = globalvar.ORDER_SIDE_SELL

        precision = int(crypto.asset['decimals'])
        order_data = {
            'ordertype': 'market',
            'side': side,
            'pair': crypto.pair,
            'amount': float(f'{float(amount):.{precision}f}'),
            'crypto': crypto,
            'validate': False,  # Test variable
        }

        response = self.create_order(order_data)

        print(response)

        if side == globalvar.ORDER_SIDE_BUY:
            self.cost_handler.buy(crypto)
        else:
            self.cost_handler.sell(crypto)

    def get_balances(self, wallet: dict) -> dict:
        with self.get_user() as user:
            balances = user.get_balances()

        for key in balances.keys():
            if key not in wallet.keys():
                wallet[key] = Crypto(key)
            wallet[key].balance = float(balances[key]['balance'])
        return wallet

    def assets(self, wallet: dict):
        url = f'https://api.kraken.com/0/public/Assets'

        response = requests.get(url)

        response_data = response.json()
        response.close()

        if response_data['error'] and self.times < 3:
            sleep(5)
            self.assets(wallet)
        self.times = 0

        codes = wallet.keys() if wallet != {} else response_data['result'].keys()
        for code in codes:
            currency_code = response_data['result'][code]['altname']
            if currency_code in wallet.keys():
                if response_data['result'][code]['status'] != 'enabled':
                    del wallet[currency_code]
                    continue
                wallet[currency_code].asset = response_data['result'][code]
        return self.pairs(wallet=wallet)

    def pairs(self, wallet: dict):
        url = f'https://api.kraken.com/0/public/AssetPairs'
        response = requests.get(url)

        response_data = response.json()
        response.close()

        if response_data['error'] and self.times < 3:
            sleep(5)
            self.pairs(wallet=wallet)
        self.times = 0

        pairs_data = response_data['result']
        for code in pairs_data.keys():
            currency_code = pairs_data[code]['base']
            if currency_code in wallet.keys() and pairs_data[code]['quote'] == 'ZEUR':
                if pairs_data[code]['status'] != 'online':
                    del wallet[currency_code]
                    continue
                wallet[currency_code].pair = pairs_data[code]
                wallet[currency_code].trade_amount_min = float(pairs_data[code]['ordermin'])
        return wallet

    def ticker(self, wallet=None) -> dict:
        url = f'https://api.kraken.com/0/public/Ticker'
        response = requests.get(url)

        response_data = response.json()
        response.close()
        if response_data['error'] and self.times < 3:
            self.times += 1
            sleep(5)
            self.ticker(wallet)
        self.times = 0

        crypto_data = response_data['result']
        for code in wallet.keys():
            currency_code = f'{code}{globalvar.DEFAULT_CURRENCY}'
            if wallet[code] == crypto_data.keys():
                wallet[code].set_rate(crypto_data[currency_code]['c'][0])
        return wallet

    def create_order(self, order_data):
        print(f'{self.glv.tracker} {order_data["side"]} | {order_data["amount"]}')
        print(order_data, order_data['crypto'].instrument)

        if globalvar.TEST:
            order_data['validate'] = True

        return self.get_client().create_order(
            ordertype=order_data['ordertype'],
            side=order_data['side'],
            pair=order_data['pair'],
            volume=order_data['amount'],
            validate=order_data['validate']
        )
