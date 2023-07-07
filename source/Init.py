import asyncio
import json
from Crypto import Crypto
import globalvar


class Init:
    def __init__(self, bitpanda):
        self.bitpanda = bitpanda

    def fill_wallet(self, wallet) -> dict:
        # self.load_file(wallet)

        if globalvar.get_ip() == globalvar.IP_WORK:
            wallet['BTC'] = Crypto('BTC')
            wallet['BTC'].rate = None
            wallet['BTC'].top_rate = None
            wallet['BTC'].last_rate = None
            wallet['BTC'].amount += 0.0003

            wallet['SHIB'] = Crypto('SHIB')
            wallet['SHIB'].rate = None
            wallet['SHIB'].top_rate = None
            wallet['SHIB'].last_rate = None
            wallet['SHIB'].amount += 0.0004
            return wallet

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.bitpanda.get_balances())

        for crypto in response:
            if crypto['currency_code'] not in wallet.keys():
                wallet[crypto['currency_code']] = Crypto(crypto['currency_code'])
                wallet[crypto['currency_code']].rate = None
                wallet[crypto['currency_code']].top_rate = None
                wallet[crypto['currency_code']].last_rate = None
            wallet[crypto['currency_code']].amount += float(crypto['available'])

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
