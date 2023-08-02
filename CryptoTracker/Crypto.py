
class Crypto:
    def __init__(self, code):
        self.code = code
        self.rate = None
        self.last_rate = None
        self.buy_rate = None
        self.sell_rate = None
        self.top_rate = None
        self.amount = 0
        self.amount_euro = 0
        self.buy_amount_euro = 0
        self.profit = 0
        self.profit_euro = 0
        self.asset = None
        self.pair = None
        self.balance = None
        self.trade_amount_min = 0

        # Percentages
        self.available = 0
        self.sells = 0
        self.gain = 0

        # Steps
        self.position = 0
        self.drops = 0

    def set_rate(self, rate):
        if self.rate is not None:
            self.last_rate = self.rate

        self.rate = float(rate)

        if self.top_rate is None:
            self.top_rate = self.rate
            self.buy_rate = self.rate

        self.amount_euro = self.balance / self.rate
        self.top_rate = self.rate if self.rate > self.top_rate else self.top_rate

    def print_variables(self, tracker):
        print(f'Exchange: {tracker}')
        print(f'code: {self.code}')
        print(f'buy_rate: {self.buy_rate}')
        print(f'sell_rate: {self.rate}')
        print(f'top_rate: {self.top_rate}')
        print(f'value_drops: {self.drops}')
        print(f'profit: {float(self.profit):.15f}')
        print('--------------------------------')
