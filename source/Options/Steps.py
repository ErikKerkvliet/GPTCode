import source.globalvar as globalvar
from bitpanda.enums import OrderSide


class Steps:
    def __init__(self, glv):
        self.bitpanda = glv.get_bitpanda()

    @staticmethod
    def calculate(crypto):
        if crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return

        profit = crypto.rate > crypto.last_rate
        if profit:
            if crypto.position < 0:
                crypto.position = 1
                crypto.more += 1
            else:
                crypto.position += 1

        if not profit:
            crypto.position -= 1
            if crypto.position > 0:
                crypto.less += 1

        if not profit \
                and crypto.position <= 3 \
                and (crypto.rate / crypto.buy_rate) * globalvar.BITPANDA_MARGIN > 1:
            return OrderSide.SELL.value
        return False
