from Bitpanda import Bitpanda
from Crypto import Crypto
import globalvar


class Trade:
    def __init__(self):
        self.bitpanda = Bitpanda(globalvar.Globalvar())

    def sell(self, crypto_code, amount):
        crypto = Crypto(crypto_code)
        crypto.amount = amount / self.bitpanda.ticker(crypto_code)

        instrument = self.bitpanda.get_instrument(crypto)

        instrument = [d for d in instrument if d.get('code') == crypto_code][0]
        crypto.instrument = instrument

        self.bitpanda.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        crypto = Crypto(crypto_code)
        crypto.amount = (amount / float(self.bitpanda.ticker(crypto_code)[crypto_code]))

        crypto.rate = float(self.bitpanda.ticker(crypto_code)[crypto_code])
        crypto.buy_rate = crypto.rate
        crypto.buy_amount_euro = amount
        instrument = self.bitpanda.get_instrument(crypto.code)

        crypto.instrument = instrument
        self.bitpanda.start_transaction(crypto, globalvar.ORDER_SIDE_BUY)
        self.bitpanda.close_client()
        print('done')

