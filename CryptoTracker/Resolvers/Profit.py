from packages.bitpanda.enums import OrderSide


class Profit:
    def __init__(self, glv):
        self.glv = glv

    @staticmethod
    def resolve(crypto):
        if crypto.buy_rate < crypto.rate * 1.0:
            pass


