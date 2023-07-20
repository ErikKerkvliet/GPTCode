import globalvar


class Crypto:
    def __init__(self, code):
        self.code = code
        self.rate = None
        self.last_rate = None
        self.buy_rate = 0
        self.buy_rate_euro = 0
        self.top_rate = 0
        self.amount = 0
        self.amount_euro = 0
        self.profit = 0
        self.profit_euro = 0
        self.instrument = None
        self.pair = None

        # Percentages
        self.value_drops = 0
        self.available = 0
        self.sells = 0
        self.gain = 0

        # Steps
        self.position = 0

    def reset(self):
        self.buy_rate = 0
        self.top_rate = 0
        self.last_rate = 0
        self.value_drops = 0

    def set_rate(self, rate):
        if self.rate is not None:
            self.last_rate = self.rate

        self.rate = float(rate)

        if self.top_rate is None:
            self.top_rate = self.rate
            self.buy_rate = self.rate
            self.buy_rate_euro = globalvar.BUY_AMOUNT / self.buy_rate

        self.top_rate = self.rate if self.rate >= self.top_rate else self.top_rate

    def up(self, response):
        self.amount_euro = response['amount_euro']
        self.buy_rate = response['rate']
        self.top_rate = self.buy_rate
        self.last_rate = self.buy_rate
        self.amount = float(response['amount'])
        self.available += float(response['amount'])

    def print_variables(self):
        print(f'code: {self.code}')
        print(f'buy_rate: {self.buy_rate}')
        print(f'sell_rate: {self.rate}')
        print(f'top_rate: {self.top_rate}')
        print(f'value_drops: {self.value_drops}')
        print(f'available: {float(self.available):.15f}')
        print(f'profit: {float(self.profit):.15f}')
        print('--------------------------------')
