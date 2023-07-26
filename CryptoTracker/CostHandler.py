from Crypto import Crypto
import globalvar


class CostHandler:
    def __init__(self):
        pass

    @staticmethod
    def buy(crypto: Crypto):
        crypto.amount = globalvar.BUY_AMOUNT / crypto.rate
        crypto.amount_euro = globalvar.BUY_AMOUNT
        crypto.buy_amount_euro = globalvar.BUY_AMOUNT
        crypto.buy_rate = crypto.rate

    @staticmethod
    def sell(crypto: Crypto):
        crypto.profit += crypto.amount * (crypto.rate - crypto.buy_rate) * globalvar.MARGIN

        amount = float(crypto.rate) * float(crypto.amount)
        rate = crypto.rate if crypto.rate > 0 else crypto.rate + 1
        buy_rate = crypto.buy_rate if crypto.buy_rate > 0 else crypto.buy_rate + 1

        crypto.profit_euro += (crypto.amount * rate) - (crypto.amount * buy_rate) * globalvar.MARGIN

        crypto.sells += 1
        crypto.amount = 0
        crypto.amount_euro = 0
        crypto.position = 0
        crypto.drops = 0
