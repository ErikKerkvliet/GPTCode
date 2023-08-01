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
        crypto = self.exchanges[self.current_exchange].ticker(wallet=wallet)[crypto_code]

        crypto.amount = amount / crypto.rate

        assets = self.exchanges[self.current_exchange].assets(wallet)
        asset = [d for d in assets if d.get('code') == crypto_code][0]
        crypto.asset = asset

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        crypto = self.exchanges[self.current_exchange].ticker(wallet=wallet)[crypto_code]

        if amount:
            crypto.buy_amount_euro = amount
            crypto.buy_rate = amount

        crypto.asset = self.exchanges[self.current_exchange].assets(wallet=wallet)

        self.exchanges[self.current_exchange].start_transaction(crypto, globalvar.ORDER_SIDE_BUY)

        if self.current_exchange == 'Bitpanda':
            self.exchanges[self.current_exchange].close_client()
        print('done')
