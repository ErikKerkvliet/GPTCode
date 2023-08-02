import globalvar


class Steps:
    def __init__(self, glv):
        self.glv = glv

    def resolve_sell(self, crypto) -> bool:
        # crypto.print_variables(self.glv.tracker)
        # print(crypto.balance == 0, crypto.last_rate is None, crypto.rate == crypto.last_rate)
        if crypto.rate is not None:
            code = crypto.code if len(crypto.code) == 4 else f'{crypto.code} '
            diff = crypto.buy_rate / crypto.rate
            difference = -(1 - diff) if diff < 1 else (diff - 1) * 100
            print(f'Coin: {code}, Difference: {difference}%')

        if crypto.balance == 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
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
                    and crypto.rate < crypto.last_rate * globalvar.SELL_MARGIN:
                print('SELL!!!!!!!!!!!!!!!!!!!', 2)
                return True
        return False

    @staticmethod
    def resolve_buy(crypto) -> bool:
        if crypto.balance != 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return False
        if crypto.position > 2 \
                and crypto.sell_rate is not None \
                or crypto.sell_rate < crypto.rate * globalvar.BUY_MARGIN:
            return True
        return False


    @staticmethod
    def calc(var1, var2) -> float:
        return var1 / var2 if var2 > 1 else var1 * var2
