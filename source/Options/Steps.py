import source.globalvar as globalvar
from packages.bitpanda.enums import OrderSide


class Steps:
    @staticmethod
    def calculate(crypto):
        if crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return

        profit = crypto.rate > crypto.last_rate
        if profit:
            if crypto.buy_rate < crypto.rate and crypto.position < 0:
                crypto.position = 1
            elif crypto.buy_rate < crypto.rate:
                crypto.position += 1

        if not profit:
            if crypto.buy_rate > crypto.rate and crypto.position > 0:
                crypto.position = -1
            elif crypto.buy_rate > crypto.rate:
                crypto.position -= 1

            if crypto.position > 3 \
                    and crypto.buy_rate < crypto.rate \
                    and crypto.rate - crypto.buy_rate > (crypto.top_rate - crypto.buy_rate) * 0.8:
                return OrderSide.SELL.value

            if crypto.position > 3 and crypto.buy_rate < (crypto.rate * globalvar.BITPANDA_MARGIN):
                return OrderSide.SELL.value

        return False
