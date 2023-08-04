from Bitpanda import Bitpanda
from Crypto import Crypto
import globalvar
from Kraken import Kraken
from OneTrading import OneTrading


class Trade:
    def __init__(self):
        self.glv = globalvar.Globalvar()

        self.current_exchange = globalvar.EXCHANGES_KRAKEN
        self.glv.tracker = self.current_exchange

        self.exchanges = {
            globalvar.EXCHANGES_BITPANDA: Bitpanda(self.glv),
            globalvar.EXCHANGES_KRAKEN: Kraken(self.glv),
            globalvar.EXCHANGES_ONE_TRADING: OneTrading(self.glv),
        }

    def sell(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        wallet[crypto_code].balance = 0

        wallet = self.exchanges[self.current_exchange].fill_assets(wallet)
        crypto = self.exchanges[self.current_exchange].ticker(wallet=wallet)[crypto_code]

        crypto.balance = amount / crypto.rate

        self.exchange.start_transaction(crypto, globalvar.ORDER_SIDE_SELL)

    def buy(self, crypto_code, amount):
        wallet = {crypto_code: Crypto(crypto_code)}
        wallet[crypto_code].balance = 0

        wallet = self.exchanges[self.current_exchange].fill_assets(wallet=wallet)
        crypto = self.exchanges[self.current_exchange].ticker(wallet=wallet)[crypto_code]

        if amount:
            crypto.buy_amount_euro = amount
            crypto.buy_rate = amount

        self.exchanges[self.current_exchange].start_transaction(crypto, globalvar.ORDER_SIDE_BUY)

        if self.current_exchange == globalvar.EXCHANGES_BITPANDA:
            self.exchanges[self.current_exchange].close_client()
        print('done')
