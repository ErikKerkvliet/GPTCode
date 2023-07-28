import globalvar
from Fill import Fill


class KrakenTracker:
    def __init__(self, glv):
        self.glv = glv
        self.glv.tracker = globalvar.EXCHANGES_KRAKEN
        self.wallet = {}
        self.fill = Fill(self.glv)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_KRAKEN)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)

    def track(self, times):
        if times % 10 == 0:
            print(f'Kraken - times: {times}')

        self.glv.tracker = globalvar.EXCHANGES_KRAKEN
        if times % 25 == 0:
            self.wallet = self.fill.fill_wallet(self.wallet)
            self.exchange.pairs = self.exchange.asset_pairs()

        self.wallet = self.exchange.ticker(None, self.wallet)
        for crypto in self.wallet.keys():
            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_SELL)

                self.exchange.start_transaction(self.wallet[crypto], globalvar.BUY_AMOUNT, globalvar.ORDER_SIDE_BUY)

            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_BUY)
