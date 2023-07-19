import globalvar as globalvar


class Steps:
    def __init__(self, glv):
        self.glv = glv

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
                    and crypto.rate - crypto.buy_rate > (crypto.top_rate - crypto.buy_rate) * 0.8 \
                    and crypto.rate * crypto.amount > crypto.instrument['min_size']:
                return globalvar.ORDER_SIDE_SELL

            if crypto.position > 3 and crypto.buy_rate < (crypto.rate * globalvar.MARGIN):
                return globalvar.ORDER_SIDE_BUY

        return False