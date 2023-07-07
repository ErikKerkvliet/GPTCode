import globalvar


class Crypto:
    def __init__(self, code):
        self.code = code
        self.rate = None
        self.last_rate = None
        self.buy_rate = 0
        self.top_rate = 0
        self.amount = 0

        # Percentages
        self.value_drops = 0
        self.amount_euro = 0
        self.profit = 0
        self.available = 0
        self.sells = 0
        self.gain = 0

        # Steps
        self.up_down = 0
        self.down_up = 0
        self.position = 0

    def reset(self):
        self.buy_rate = 0
        self.top_rate = 0
        self.last_rate = 0
        self.value_drops = 0

    def set_rate(self, crypto):
        if self.rate is not None:
            self.last_rate = self.rate

        self.rate = float(crypto[globalvar.DEFAULT_CURRENCY])

        if self.top_rate is None:
            self.top_rate = self.rate
            self.buy_rate = self.rate

        self.top_rate = self.rate if self.rate > self.top_rate else self.top_rate

    def get_sell_amount(self):
        self.sells += 1
        amount = self.available * globalvar.SELL_PERC
        if self.sells % 10 == 0:
            self.gain += self.rate - self.buy_rate
            amount = self.available - amount
            self.profit = 0
            return amount
        else:
            return amount

    def up(self, response):
        self.amount_euro = response['amount_euro']
        self.buy_rate = response['rate']
        self.top_rate = self.buy_rate
        self.last_rate = self.buy_rate
        self.amount = float(response['amount'])
        self.available += float(response['amount'])

    def lower(self, amount=None):
        if amount:
            self.available -= amount
        else:
            amount = self.available * (1 - (globalvar.SELL_PERC - globalvar.BITPANDA_PERC))
            self.profit += (self.available - amount)
            self.available -= amount

    def print_variables(self):
        print(f'code: {self.code}')
        print(f'buy_rate: {self.buy_rate}')
        print(f'sell_rate: {self.rate}')
        print(f'top_rate: {self.top_rate}')
        print(f'value_drops: {self.value_drops}')
        print(f'available: {float(self.available):.15f}')
        print(f'profit: {float(self.profit):.15f}')
        print('--------------------------------')
