import asyncio
import json
from Crypto import Crypto
import globalvar


class Init:
    def __init__(self, bitpanda):
        self.bitpanda = bitpanda

    def fill_wallet(self, wallet) -> dict:
        # self.load_file(wallet)

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.bitpanda.get_balances())

        for crypto in response:
            if crypto['currency_code'] not in wallet.keys():
                wallet[crypto['currency_code']] = Crypto(crypto['currency_code'])
                wallet[crypto['currency_code']].rate = 1
                wallet[crypto['currency_code']].top_rate = 1
                wallet[crypto['currency_code']].last_rate = 1
            wallet[crypto['currency_code']].available += float(crypto['available'])

        return wallet

    @staticmethod
    def load_file(wallet):
        with open(globalvar.SAVE_FILE, 'r') as file:
            data = json.load(file)
            file.close()

        for crypto in data:
            if crypto['code'] == globalvar.DEFAULT_CURRENCY:
                wallet[crypto['code']] = Crypto(crypto['code'])
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].buy_rate = crypto['buy_rate']
            # wallet[crypto['code']].value_drops = crypto['drops']
            wallet[crypto['code']].amount = crypto['amount']
            wallet[crypto['code']].profit = crypto['profit']
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].sells = crypto['sells']
            wallet[crypto['code']].amount_euro = crypto['amount_€']
        return wallet
