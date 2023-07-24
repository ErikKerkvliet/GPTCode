import globalvar


class Steps:
    def __init__(self, glv):
        self.glv = glv

    @staticmethod
    def resolve(crypto):
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
                    and crypto.amount < crypto.amount_euro / crypto.rate \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN:
                return globalvar.ORDER_SIDE_SELL

        return False
