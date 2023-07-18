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
        self.init.fill_wallet()
        wallet = self.glv.get_wallet()
        data = self.exchange.ticker()
        print(self.glv.wallet['ZEUR'].amount)

        if times % 10 == 0:
            print(f'Times: {times} | Rate BTC: {float(data["TBTC"].amount):.2f}')

        for crypto in wallet.keys():
            print(data)
            exit()
            self.wallet[crypto].set_rate(data[crypto])

            result = self.option.calculate(wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.sell(wallet[crypto])

                self.exchange.buy(wallet[crypto], 15)

            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.buy(wallet[crypto])
        self.store.save()
        exit()
