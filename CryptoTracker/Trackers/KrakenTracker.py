import globalvar
from Init import Init


class KrakenTracker:
    def __init__(self, glv):
        self.glv = glv
        self.glv.tracker = globalvar.EXCHANGES_KRAKEN
        self.wallet = {}
        self.init = Init(self.glv)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_KRAKEN)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)

    def track(self, times):
        if times % 10 == 0:
            print(f'Kraken - times: {times}')

        self.glv.tracker = globalvar.EXCHANGES_KRAKEN
        if times % 25 == 0:
            self.wallet = self.init.fill_wallet(self.wallet)
        self.wallet = self.exchange.ticker(None, self.wallet)
        for crypto in self.wallet.keys():
            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.sell(self.wallet[crypto])

                self.exchange.buy(self.wallet[crypto], globalvar.BUY_AMOUNT)

            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.buy(self.wallet[crypto])
