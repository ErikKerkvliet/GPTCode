import asyncio
import json
from Crypto import Crypto
import globalvar


class Init:
    def __init__(self, glv):
        self.glv = glv
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)

    def fill_wallet(self, wallet):
        # self.from_file(wallet)

        if globalvar.TEST:
            return self.from_test(wallet)
        elif globalvar.EXCHANGE == globalvar.EXCHANGES_KRAKEN:
            return self.from_kraken_balance(wallet)
        elif globalvar.get_ip() == globalvar.IP_WORK:
            return self.from_work(wallet)
        elif globalvar.get_ip() == globalvar.IP_HOME:
            if globalvar.EXCHANGE == globalvar.EXCHANGES_BITPANDA:
                return self.from_bitpanda_balance(wallet)
            elif globalvar.EXCHANGE == globalvar.EXCHANGES_KRAKEN:
                return self.from_kraken_balance(wallet)

    def from_bitpanda_balance(self, wallet) -> dict:
        loop = asyncio.get_event_loop()
        instruments = self.glv.exchanges.get_instrument()
        response = loop.run_until_complete(self.glv.exchanges.get_balances())

        for crypto in response:
            if crypto['currency_code'] == 'EUR' or instruments[crypto['currency_code']]['state'] != 'ACTIVE':
                continue
            if crypto['currency_code'] == 'BTC' or crypto['currency_code'] == 'BEST':
                continue

            if crypto['currency_code'] not in wallet.keys():
                wallet[crypto['currency_code']] = Crypto(crypto['currency_code'])
                wallet[crypto['currency_code']].instrument = instruments[crypto['currency_code']]
                wallet[crypto['currency_code']].pair = f'{crypto["currency_code"]}{globalvar.DEFAULT_CURRENCY}'
                wallet[crypto['currency_code']].rate = None
                wallet[crypto['currency_code']].top_rate = None
                wallet[crypto['currency_code']].last_rate = None
            wallet[crypto['currency_code']].amount += float(crypto['available'])
        return wallet

    def from_kraken_balance(self, wallet) -> dict:
        balances = self.glv.exchanges[globalvar.EXCHANGES_KRAKEN].get_balances()
        for full_code in balances.keys():
            code = f'{full_code}Z' if full_code[0:2] == 'XX' or 'XE' else full_code
            if code == globalvar.DEFAULT_CURRENCY:
                continue
            if full_code not in wallet.keys():
                wallet[code] = Crypto(code)
                wallet[code].pair = f'{full_code}{globalvar.DEFAULT_CURRENCY}'
                wallet[code].rate = None
                wallet[code].top_rate = None
                wallet[code].last_rate = None
            wallet[code].amount += float(balances[full_code])
        return wallet

    def from_file(self, wallet) -> dict:
        with open(globalvar.SAVE_FILE, 'r') as file:
            data = json.load(file)
            file.close()

        for crypto in data:
            if crypto['code'] != globalvar.DEFAULT_CURRENCY:
                wallet[crypto['code']] = Crypto(crypto['code'])
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].buy_rate = crypto['buy_rate']
            wallet[crypto['code']].amount = crypto['amount']
            wallet[crypto['code']].profit = crypto['profit']
            wallet[crypto['code']].available = crypto['available']
            wallet[crypto['code']].amount_euro = crypto['amount_€']
        return wallet

    def from_work(self, wallet) -> dict:
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
        return wallet

    def from_test(self, wallet) -> dict:
        response = self.exchange.ticker()
        for crypto in response.keys():
            if crypto not in wallet.keys() and crypto not in globalvar.DEFAULT_CURRENCY:
                amount = float(response[crypto])
                wallet[crypto] = Crypto(crypto)
                wallet[crypto].instrument = {'min_size': 0, 'amount_precision': 5}
                wallet[crypto].pair = f'{crypto}{globalvar.DEFAULT_CURRENCY}'
                wallet[crypto].amount = amount * 15
                wallet[crypto].rate = amount
                wallet[crypto].top_rate = amount
                wallet[crypto].last_rate = amount
                wallet[crypto].buy_rate = amount
        return wallet
