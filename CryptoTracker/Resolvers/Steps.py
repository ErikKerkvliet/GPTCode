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
            if crypto.position < 0:
                crypto.position = 1
            else:
                crypto.position += 1

            if crypto.drops > 0:
                crypto.drops -= 1

        if not profit:
            if crypto.position > 0:
                crypto.position = -1
            else:
                crypto.position -= 1

            if crypto.drops < 3:
                crypto.drops += 1

            print(crypto.amount_euro, crypto.rate, crypto.trade_amount_min)
            if crypto.drops > 2 \
                    and crypto.amount_euro / crypto.rate > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN:
                print('SELL!!!!!!!!!!!!!!!!!!!', 1)
                return globalvar.ORDER_SIDE_SELL

            if crypto.amount_euro / crypto.rate > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN \
                    and crypto.rate < crypto.top_rate * 0.999:
                print('SELL!!!!!!!!!!!!!!!!!!!', 2)
                return globalvar.ORDER_SIDE_SELL
        return False
