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
        self.glv.tracker = globalvar.EXCHANGES_KRAKEN
        if times % 25 == 0:
            self.wallet = self.init.fill_wallet(self.wallet)
        data = self.exchange.ticker()

        if times % 10 == 0:
            print(f'Kraken - times: {times}')
        for crypto in self.wallet.keys():
            self.wallet[crypto].set_rate(data[crypto])

            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.sell(self.wallet[crypto])

                self.exchange.buy(self.wallet[crypto], 15)

            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.buy(self.wallet[crypto])
