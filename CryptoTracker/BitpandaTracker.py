import asyncio

import globalvar
from Init import Init


class BitpandaTracker:
    def __init__(self, glv):
        self.glv = glv
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_BITPANDA)
        self.init = Init(self.glv)
        self.wallet = self.glv.get_wallet()
        self.option = self.glv.get_option()
        self.store = self.glv.store

    def track(self, times):

        self.init.fill_wallet()

        data = self.exchange.ticker()

        if times % 10 == 0:
            print(f'Times: {times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO][globalvar.DEFAULT_CURRENCY]):.2f}')

        loop = asyncio.get_event_loop()
        for crypto in self.wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue

            self.wallet[crypto].set_rate(data[crypto])

            result = self.option.calculate(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                loop.run_until_complete(self.exchange.sell(self.wallet[crypto]))

                loop.run_until_complete(self.exchange.buy(self.wallet[crypto], 15))

            elif result == globalvar.ORDER_SIDE_BUY:
                loop.run_until_complete(self.exchange.buy(self.wallet[crypto]))

        loop.run_until_complete(self.exchange.close_client())

        self.store.save()
        self.exchange.instruments = {}
