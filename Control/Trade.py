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
        crypto = Crypto(crypto_code)
        crypto.amount = amount / self.exchange.ticker(crypto_code)

        if self.current_exchange == 'bitpanda':
            instrument = self.exchange.get_instrument(crypto)
            instrument = [d for d in instrument if d.get('code') == crypto_code][0]
            crypto.instrument = instrument

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        self.wallet = self.fill.fill_wallet(self.wallet)

        if amount:
            self.wallet[crypto_code].buy_amount_euro = amount

        if self.current_exchange == 'bitpanda':
            self.wallet[crypto_code].instrument = self.exchange.get_instrument(self.wallet[crypto_code].code)

        self.exchange.start_transaction(self.wallet[crypto_code], globalvar.ORDER_SIDE_BUY)

        if self.current_exchange == 'bitpanda':
            self.exchange.close_client()
        print('done')

