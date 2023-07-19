import globalvar


class Percentages:
    def __init__(self, glv):
        self.glv = glv
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)

    def calculate(self, wallet, code):
        buy_diff_perc = ((wallet[code].rate - wallet[code].buy_rate) / wallet[code].buy_rate)
        top_diff_perc = ((wallet[code].rate - wallet[code].top_rate) / wallet[code].top_rate)
        last_diff_perc = ((wallet[code].rate - wallet[code].last_rate) / wallet[code].last_rate)

        # if globalvar.TEST:
        #     self.exchange.sell(wallet[code])
        #     wallet[code].lower()
        #     wallet[code].print_variables()
        #     wallet[code].reset()
        #
        #     response = self.exchange.buy(wallet[code])
        #     wallet[code].up(response)
        #     continue

        if buy_diff_perc > globalvar.PROFIT_PERC:
            if wallet[code].value_drops >= globalvar.MAX_DROPS or top_diff_perc > globalvar.LOSS_PERC:
                self.exchange.sell(wallet[code])
                wallet[code].reset()

                response = self.exchange.buy(wallet[code])
                wallet[code].up(response)

        if last_diff_perc < 0:
            if wallet[code].rate > wallet[code].last_rate and wallet[code].value_drops > 0:
                wallet[code].value_drops = 0
            else:
                wallet[code].value_drops += 1

        wallet[code].last_rate = wallet[code].rate
