import asyncio

import globalvar
from Init import Init


class BitpandaTracker:
    def __init__(self, glv):
        self.glv = glv
        self.wallet = {}
        self.init = Init(self.glv)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER_STEPS)

    def track(self, times):
        self.wallet = self.init.fill_wallet(self.wallet)
        data = self.exchange.ticker()

        if times % 10 == 0:
            print(f'Times: {times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO]):.2f}')

        loop = asyncio.get_event_loop()
        for crypto in self.wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue

            self.wallet[crypto].set_rate(data[crypto])

            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                loop.run_until_complete(self.exchange.sell(self.wallet[crypto]))

                loop.run_until_complete(self.exchange.buy(self.wallet[crypto], 15))

            elif result == globalvar.ORDER_SIDE_BUY:
                loop.run_until_complete(self.exchange.buy(self.wallet[crypto]))

        loop.run_until_complete(self.exchange.close_client())

        self.exchange.instruments = {}
