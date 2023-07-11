import source.globalvar as globalvar
from packages.bitpanda.enums import OrderSide


class Profit:
    @staticmethod
    def calculate(crypto):
        if crypto.buy_rate < crypto.rate * 1.0:
            pass


