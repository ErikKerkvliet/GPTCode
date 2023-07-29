from Crypto import Crypto
from Fill import Fill
import globalvar


class Trade:
    def __init__(self):
        self.glv = globalvar.Globalvar()

        self.current_exchange = 'bitpanda'
        self.glv.tracker = self.current_exchange
        self.fill = Fill(self.glv)
        self.exchange = self.glv.get_exchange(self.glv.tracker)
        self.wallet = {}

    def sell(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        crypto = self.exchange.ticker(crypto_code=crypto_code, wallet=wallet)[crypto_code]

        crypto.amount = amount / crypto.rate

        if self.current_exchange == 'bitpanda':
            instrument = self.exchange.get_instrument(crypto)
            instrument = [d for d in instrument if d.get('code') == crypto_code][0]
            crypto.instrument = instrument

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        crypto = self.exchange.ticker(crypto_code=crypto_code, wallet=wallet)[crypto_code]

        if amount:
            crypto.buy_amount_euro = amount
            crypto.buy_rate = amount

        if self.current_exchange == 'bitpanda':
            crypto.instrument = self.exchange.get_instruments(code=crypto.code)

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_BUY)

        if self.current_exchange == 'bitpanda':
            self.exchange.close_client()
        print('done')

