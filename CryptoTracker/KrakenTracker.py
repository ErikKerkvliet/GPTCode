import globalvar
from Init import Init


class KrakenTracker:
    def __init__(self, glv):
        self.glv = glv
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_KRAKEN)
        self.init = Init(self.glv)
        self.wallet = self.glv.get_wallet()
        self.option = self.glv.get_option()
        self.store = self.glv.store

    def track(self, times):
        self.wallet = self.init.fill_wallet()
        data = self.exchange.ticker()

        if times % 10 == 0:
            print(f'Times: {times} | Rate BTC: {float(data["XXBTZEUR"]):.2f}')

        for crypto in self.wallet.keys():
            self.wallet[crypto].set_rate(data[crypto])

            result = self.option.calculate(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.sell(self.wallet[crypto])

                self.exchange.buy(self.wallet[crypto], 15)

            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.buy(self.wallet[crypto])
        self.glv.wallet = self.wallet
