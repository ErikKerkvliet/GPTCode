import json
from Crypto import Crypto
import globalvar


class Fill:
    def __init__(self, glv):
        self.glv = glv
        self.exchange = None

    def fill_wallet(self, exchange) -> dict:
        self.exchange = exchange
        wallet = {}

        if self.glv.tracker == globalvar.EXCHANGES_KRAKEN:
            return self.from_kraken_balance(wallet)
        elif self.glv.tracker == globalvar.EXCHANGES_BITPANDA:
            return self.from_bitpanda_balance(wallet)
        elif self.glv.tracker == globalvar.EXCHANGES_ONE_TRADING:
            return self.from_one_trading_balance(wallet)
        return self.from_file(wallet)

    def from_bitpanda_balance(self, wallet) -> dict:
        wallet = self.exchange.get_balances(wallet=wallet)
        for code in wallet:
            if wallet[code].code == globalvar.DEFAULT_CURRENCY:
                self.glv.balance_euro[self.glv.tracker] = wallet[code].balance
                wallet[code] = None
                continue
            wallet[code].buy_amount_euro = globalvar.BUY_AMOUNT
        return {key: value for key, value in wallet.items() if value is not None}

    def from_one_trading_balance(self, wallet) -> dict:
        pass

    def from_kraken_balance(self, wallet: dict) -> dict:
        wallet = self.exchange.get_balances(wallet=wallet)
        for code in wallet:
            if wallet[code].code[:1] == 'Z':
                self.glv.balance_euro[self.glv.tracker] = wallet[code].balance
                wallet[code] = None
                continue
            wallet[code].buy_amount_euro = globalvar.BUY_AMOUNT
        return {key: value for key, value in wallet.items() if value is not None}

    def from_file(self, wallet) -> dict:
        save_file = f'{globalvar.SAVE_FILE}_{self.glv.tracker}'
        with open(save_file, 'r') as file:
            data = json.load(file)
            file.close()

        del data[0]
        for crypto in data:
            if crypto['code'] in wallet.keys():
                wallet[crypto['code']].buy_rate = crypto['buy_rate']
                wallet[crypto['code']].top_rate = crypto['top_rate']
                wallet[crypto['code']].last_rate = crypto['last_rate']
        return wallet

    @staticmethod
    def from_work() -> dict:
        wallet = {'BTC': Crypto('BTC')}
        wallet['BTC'].rate = None
        wallet['BTC'].top_rate = None
        wallet['BTC'].last_rate = None
        wallet['BTC'].balance += 0.0003

        wallet['SHIB'] = Crypto('SHIB')
        wallet['SHIB'].rate = None
        wallet['SHIB'].top_rate = None
        wallet['SHIB'].last_rate = None
        wallet['SHIB'].balance += 0.0004
        return wallet

    def from_test(self, wallet) -> dict:
        response = self.exchange.ticker()
        for crypto in response.keys():
            if crypto not in wallet.keys():
                amount = float(response[crypto])
                wallet[crypto] = Crypto(crypto)
                wallet[crypto].instrument = {'min_size': 0, 'amount_precision': 5}
                wallet[crypto].balance = amount * 15
                wallet[crypto].last_rate = amount
        return wallet
