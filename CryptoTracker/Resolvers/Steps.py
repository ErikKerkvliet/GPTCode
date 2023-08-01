import globalvar


class Steps:
    def __init__(self, glv):
        self.glv = glv

    def resolve_sell(self, crypto) -> bool:
        if crypto.amount == 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return False
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

            if crypto.drops < 2:
                crypto.drops += 1

            if crypto.drops > 2 \
                    and self.calc(crypto.amount_euro, crypto.rate) > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN:

                print('SELL!!!!!!!!!!!!!!!!!!!', 1)
                return True

            if self.calc(crypto.amount_euro, crypto.rate) > crypto.trade_amount_min \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN \
                    and crypto.rate < crypto.last_rate * 0.998:
                print('SELL!!!!!!!!!!!!!!!!!!!', 2)
                return True
        return False

    @staticmethod
    def resolve_buy(crypto) -> bool:
        if crypto.amount != 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return False
        return crypto.rate > crypto.last_rate

    @staticmethod
    def calc(var1, var2) -> float:
        return var1 / var2 if var2 > 1 else var1 * var2
