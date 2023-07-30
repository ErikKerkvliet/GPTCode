from Bitpanda import Bitpanda
from Crypto import Crypto
from Fill import Fill
import globalvar
from Kraken import Kraken
from OneTrading import OneTrading


class Trade:
    def __init__(self):
        self.glv = globalvar.Globalvar()

        self.current_exchange = globalvar.EXCHANGES_BITPANDA
        self.glv.tracker = self.current_exchange
        self.fill = Fill(self.glv)
        self.exchange = self.glv.get_exchange(self.glv.tracker)
        self.wallet = {}
        self.exchanges = {
            globalvar.EXCHANGES_BITPANDA: Bitpanda(self.glv),
            globalvar.EXCHANGES_KRAKEN: Kraken(self.glv),
            globalvar.EXCHANGES_ONE_TRADING: OneTrading(self.glv),
        }

    def sell(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        crypto = self.exchanges[self.current_exchange].ticker(crypto_code=crypto_code, wallet=wallet)[crypto_code]

        crypto.amount = amount / crypto.rate

        if self.current_exchange == 'Bitpanda':
            instrument = self.exchanges[self.current_exchange].asset_pairs(code=crypto)
            instrument = [d for d in instrument if d.get('code') == crypto_code][0]
            crypto.instrument = instrument

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        crypto = self.exchanges[self.current_exchange].ticker(crypto_code=crypto_code, wallet=wallet)[crypto_code]

        if amount:
            crypto.buy_amount_euro = amount
            crypto.buy_rate = amount

        if self.current_exchange == 'Bitpanda':
            crypto.instrument = self.exchanges[self.current_exchange].asset_pairs(code=crypto.code)

        self.exchanges[self.current_exchange].start_transaction(crypto, globalvar.ORDER_SIDE_BUY)

        if self.current_exchange == 'Bitpanda':
            self.exchanges[self.current_exchange].close_client()
        print('done')

