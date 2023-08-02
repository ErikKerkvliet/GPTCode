from Crypto import Crypto
import globalvar


class CostHandler:
    def __init__(self):
        pass

    @staticmethod
    def buy(crypto: Crypto):
        crypto.balance = globalvar.BUY_AMOUNT / crypto.rate
        crypto.amount_euro = globalvar.BUY_AMOUNT
        crypto.buy_amount_euro = globalvar.BUY_AMOUNT
        crypto.buy_rate = crypto.rate
        crypto.drops = 0

    @staticmethod
    def sell(crypto: Crypto):
        crypto.profit += crypto.balance * (crypto.rate - crypto.buy_rate) * globalvar.MARGIN

        crypto.profit_euro += (crypto.balance * crypto.rate) - (crypto.balance * crypto.buy_rate) * globalvar.MARGIN

        crypto.sell_rate = crypto.rate
        crypto.sells += 1
        crypto.balance = 0
        crypto.amount_euro = 0
        crypto.position = 0
        crypto.drops = 0
