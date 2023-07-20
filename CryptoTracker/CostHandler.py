from Crypto import Crypto
import globalvar


class CostHandler:
    def __init__(self):
        pass

    @staticmethod
    def buy(crypto: Crypto):
        crypto.amount = globalvar.BUY_AMOUNT / crypto.rate
        crypto.amount_euro = globalvar.BUY_AMOUNT

        crypto.buy_rate = crypto.rate

    @staticmethod
    def sell(crypto: Crypto):
        crypto.profit += crypto.amount_euro / crypto.buy_rate
        crypto.profit_euro += globalvar.BUY_AMOUNT * (crypto.rate - crypto.buy_rate)

        crypto.sells += 1
        crypto.amount = 0
        crypto.amount_euro = 0
        crypto.position = 0
