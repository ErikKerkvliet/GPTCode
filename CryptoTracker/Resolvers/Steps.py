import globalvar


class Steps:
    def __init__(self, glv):
        self.glv = glv

    def resolve(self, crypto):
        if crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return

        if crypto.rate < 0:
            amount = crypto.amount_euro * crypto.rate
        else:
            amount = crypto.amount_euro / crypto.rate

        profit = crypto.rate > crypto.last_rate
        if profit:
            if crypto.position < 0:
                crypto.position = 1
            else:
                crypto.position += 1

            if crypto.drops > 0:
                crypto.drops -= 1

            if self.glv.times != 0 \
                    and amount > crypto.trade_amount_min \
                    and self.calc(crypto.buy_rate, crypto.rate) * globalvar.MARGIN:
                self.glv.timer = 10
                return

        if not profit:
            if crypto.position > 0:
                crypto.position = -1
            else:
                crypto.position -= 1

            if crypto.drops < 2:
                crypto.drops += 1

            # print(crypto.amount_euro, crypto.rate, crypto.trade_amount_min)

            if crypto.drops > 2 \
                    and self.calc(crypto.amount_euro, crypto.rate) > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN:

                print('SELL!!!!!!!!!!!!!!!!!!!', 1)
                return globalvar.ORDER_SIDE_SELL

            if self.calc(crypto.amount_euro, crypto.rate) > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN \
                    and crypto.rate < crypto.last_rate * 0.998:
                print('SELL!!!!!!!!!!!!!!!!!!!', 2)
                return globalvar.ORDER_SIDE_SELL
        return False

    @staticmethod
    def calc(var1, var2):
        return var1 / var2 if var2 > 1 else var1 * var2
