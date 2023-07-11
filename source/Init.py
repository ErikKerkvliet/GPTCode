import asyncio
import json
from source.Crypto import Crypto
import globalvar


class Init:
    def __init__(self, bitpanda):
        self.bitpanda = bitpanda

    def fill_wallet(self, wallet) -> dict:
        # self.from_file(wallet)

        # if globalvar.TEST:
        #     return self.from_test(wallet)

        if globalvar.get_ip() == globalvar.IP_WORK:
            return self.from_work(wallet)

        if globalvar.get_ip() == globalvar.IP_HOME:
            return self.from_balance(wallet)

    def from_balance(self, wallet):
        loop = asyncio.get_event_loop()
        # response = self.bitpanda.get_instrument()
        response = loop.run_until_complete(self.bitpanda.get_balances())

        for crypto in response:
            if crypto['currency_code'] == 'UNI' or crypto['currency_code'] == 'BTC' or crypto['currency_code'] == 'BEST':
                continue

            if crypto['currency_code'] not in wallet.keys():
                wallet[crypto['currency_code']] = Crypto(crypto['currency_code'])
                wallet[crypto['currency_code']].rate = None
                wallet[crypto['currency_code']].top_rate = None
                wallet[crypto['currency_code']].last_rate = None
            wallet[crypto['currency_code']].amount += float(crypto['available'])
        return wallet

    @staticmethod
    def from_file(wallet):
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
            wallet[crypto['code']].amount_euro = crypto['amount_€']
        return wallet

    @staticmethod
    def from_work(wallet):
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

    def from_test(self, wallet):
        response = self.bitpanda.ticker()
        for crypto in response.keys():
            if crypto not in wallet.keys():
                wallet[crypto] = Crypto(crypto)
                wallet[crypto].amount += float(response[crypto][globalvar.DEFAULT_CURRENCY])
                wallet[crypto].rate = wallet[crypto].amount
                wallet[crypto].top_rate = wallet[crypto].amount
                wallet[crypto].last_rate = wallet[crypto].amount
                wallet[crypto].buy_rate = wallet[crypto].amount
        return wallet
