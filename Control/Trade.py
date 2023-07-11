from source.Bitpanda import Bitpanda
from source.Crypto import Crypto
import source.globalvar as globalvar


class Trade:
    def __init__(self):
        self.bitpanda = Bitpanda()

    def sell(self, crypto_code, amount):
        crypto = Crypto(crypto_code)
        crypto.amount = amount / self.bitpanda.ticker(crypto_code, globalvar.DEFAULT_CURRENCY)

        instrument = self.bitpanda.get_instrument(crypto)

        instrument = [d for d in instrument if d.get('code') == crypto_code][0]
        crypto.instrument = instrument

        self.bitpanda.sell(crypto)

    def buy(self, crypto_code, amount):
        crypto = Crypto(crypto_code)
        crypto.amount = amount / self.bitpanda.ticker(crypto_code, globalvar.DEFAULT_CURRENCY)

        instruments = self.bitpanda.get_instrument(crypto)
        instrument = [d for d in instruments if d.get('code') == crypto_code][0]

        crypto.instrument = instrument

        self.bitpanda.buy(crypto)

