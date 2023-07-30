import asyncio
import json
import tracemalloc
from time import sleep
import http.client

import requests

import globalvar
import keys
from CostHandler import CostHandler


class OneTrading:
    def __init__(self, glv):
        self.glv = glv
        self.instruments = {}
        self.times = 0
        self.pairs = self.asset_pairs()
        self.cost_handler = CostHandler()

    def asset_pairs(self, crypto_code=None) -> dict:
        if self.instruments:
            if crypto_code and crypto_code != 'ALL':
                return self.instruments[crypto_code]
            else:
                return self.instruments

        url = f'http://api.onetrading.com/public/v1/instruments'
        response = requests.get(url).json()

        for instrument in response:
            self.instruments[instrument['base']['code']] = {
                'state': instrument['state'],
                'code': instrument['base']['code'],
                'precision': int(instrument['base']['precision']),
                'amount_precision': int(instrument['amount_precision']),
                'market_precision': int(instrument['market_precision']),
                'min_size': float(instrument['min_size']),
            }

        if crypto_code is None:
            return self.instruments
        return self.instruments[crypto_code]

    def ticker(self, crypto_code=None, wallet=None) -> dict:
        pair = f'{crypto_code}_EUR' if crypto_code else ''
        url = f'http://api.onetrading.com/public/v1/market-ticker/{pair}'
        response = requests.get(url)
        return {}

    def start_transaction(self, crypto, side):
        print('start_transaction')
        pass

    def get_balances(self, crypto_code=None, wallet=None) -> dict:
        if wallet is None:
            wallet = {}

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {keys.KEY_TRADE}"
        }

        response = requests.get('https://api.onetrading.com/public/v1/account/balances', headers=headers)
        response_balances = response.json()['balances']

        for balance in response_balances:
            if balance['currency_code'][-3:] == globalvar.DEFAULT_CURRENCY:
                self.glv.balance_euro[self.glv.tracker] = balance['available']
                continue
            wallet[balance['currency_code']] = balance['available']

        if crypto_code is None:
            return wallet

        return wallet[crypto_code]

    @staticmethod
    def get_balance_euro() -> float:
        return 0.0
