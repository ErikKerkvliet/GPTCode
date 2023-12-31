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
        if crypto.code[:1] == 'Z':
            return

        crypto.pair = f'{crypto.code}/{globalvar.DEFAULT_CURRENCY}'
        if side == globalvar.ORDER_SIDE_BUY:
            amount = crypto.buy_amount_euro / crypto.rate
            side = globalvar.ORDER_SIDE_BUY
        else:
            amount = crypto.balance
            side = globalvar.ORDER_SIDE_SELL

        precision = int(crypto.asset['decimals'])
        order_data = {
            'ordertype': globalvar.ORDER_TYPE,
            'side': side,
            'pair': crypto.pair,
            'amount': float(f'{float(amount):.{precision}f}'),
            'crypto': crypto,
            'price': round(globalvar.BUY_AMOUNT * globalvar.BUY_MARGIN, 2),
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

    def fill_assets(self, wallet: dict):
        url = f'https://api.kraken.com/0/public/Assets'

        response = requests.get(url)

        response_data = response.json()
        response.close()

        if response_data['error'] and self.times < 3:
            sleep(5)
            self.fill_assets(wallet)
        self.times = 0

        codes = wallet.keys() if wallet != {} else response_data['result'].keys()
        for code in codes:
            if code in wallet.keys():
                if response_data['result'][code]['status'] != 'enabled':
                    del wallet[code]
                    continue
                wallet[code].asset = response_data['result'][code]
        return self.pairs(wallet=wallet)

    def pairs(self, wallet: dict):
        url = f'https://api.kraken.com/0/public/AssetPairs'
        response = requests.get(url)

        response_data = response.json()
        response.close()

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

        for code in response_data['result'].keys():
            currency_code = code[:-4] if code[:1] == 'X' else code[:-3]
            if code[-3:] == globalvar.DEFAULT_CURRENCY and (currency_code in wallet.keys() or code[:-3] in wallet.keys()):
                wallet[currency_code].set_rate(response_data['result'][code]['c'][0])
        return wallet

    def create_order(self, order_data):
        profit_percentage = (order_data["crypto"].rate / order_data["crypto"].buy_rate) * globalvar.BUY_AMOUNT
        amount_euro = (profit_percentage - order_data["crypto"].buy_amount_euro) * globalvar.MARGIN
        print(f'=============== Kraken {order_data["side"]} | Euro: {amount_euro} ===============')
        print(order_data)

        if globalvar.TEST:
            order_data['validate'] = True

        if order_data['ordertype'] == globalvar.ORDER_TYPE_LIMIT:
            return self.get_client().create_order(
                ordertype=order_data['ordertype'],
                side=order_data['side'],
                pair=order_data['pair'],
                volume=order_data['amount'],
                validate=order_data['validate'],
                price=order_data['price']
            )
        elif order_data['ordertype'] == globalvar.ORDER_TYPE_MARKET:
            return self.get_client().create_order(
                ordertype=order_data['ordertype'],
                side=order_data['side'],
                pair=order_data['pair'],
                volume=order_data['amount'],
                validate=order_data['validate']
            )
