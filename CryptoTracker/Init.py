import asyncio
import json
from Crypto import Crypto
import globalvar


class Init:
    def __init__(self, glv):
        self.glv = glv
        self.wallet = self.glv.get_wallet()
        self.exchange = self.glv.get_exchange('bitpanda')

    def fill_wallet(self):
        # self.from_file()

        if globalvar.TEST:
            self.from_test()

        if globalvar.get_ip() == globalvar.IP_WORK:
            self.from_work()

        if globalvar.get_ip() == globalvar.IP_HOME:
            self.from_balance()

    def from_balance(self):
        wallet = {}
        loop = asyncio.get_event_loop()
        instruments = self.glv.bitpanda.get_instrument()
        response = loop.run_until_complete(self.glv.bitpanda.get_balances())

        for crypto in response:
            if crypto['currency_code'] == 'EUR' or instruments[crypto['currency_code']]['state'] != 'ACTIVE':
                continue
            if crypto['currency_code'] == 'BTC' or crypto['currency_code'] == 'BEST':
                continue

            if crypto['currency_code'] not in wallet.keys():
                wallet[crypto['currency_code']] = Crypto(crypto['currency_code'])
                wallet[crypto['currency_code']].instrument = instruments[crypto['currency_code']]
                wallet[crypto['currency_code']].rate = None
                wallet[crypto['currency_code']].top_rate = None
                wallet[crypto['currency_code']].last_rate = None
            wallet[crypto['currency_code']].amount += float(crypto['available'])
        self.wallet = wallet

    def from_file(self):
        wallet = {}
        with open(globalvar.SAVE_FILE, 'r') as file:
            data = json.load(file)
            file.close()

        for crypto in data:
            if crypto['code'] == globalvar.DEFAULT_CURRENCY:
                wallet[crypto['code']] = Crypto(crypto['code'])
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].buy_rate = crypto['buy_rate']
            wallet[crypto['code']].amount = crypto['amount']
            wallet[crypto['code']].profit = crypto['profit']
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].amount_euro = crypto['amount_€']
        self.wallet = wallet

    def from_work(self):
        wallet = {'BTC': Crypto('BTC')}
        wallet['BTC'].rate = None
        wallet['BTC'].top_rate = None
        wallet['BTC'].last_rate = None
        wallet['BTC'].amount += 0.0003

        wallet['SHIB'] = Crypto('SHIB')
        wallet['SHIB'].rate = None
        wallet['SHIB'].top_rate = None
        wallet['SHIB'].last_rate = None
        wallet['SHIB'].amount += 0.0004
        self.wallet = wallet

    def from_test(self):
        wallet = {}
        response = self.exchange.ticker()
        for crypto in response.keys():
            if crypto not in wallet.keys():
                amount = float(response[crypto][globalvar.DEFAULT_CURRENCY])
                wallet[crypto] = Crypto(crypto)
                wallet[crypto].instrument = {'min_size': 0, 'amount_precision': 5}
                wallet[crypto].amount = amount * 10
                wallet[crypto].rate = amount
                wallet[crypto].top_rate = amount
                wallet[crypto].last_rate = amount
                wallet[crypto].buy_rate = amount
        self.wallet = wallet
