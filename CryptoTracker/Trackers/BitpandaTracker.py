import asyncio

import globalvar
from Init import Init


class BitpandaTracker:
    def __init__(self, glv):
        self.glv = glv
        self.wallet = {}
        self.init = Init(self.glv)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_BITPANDA)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)

    def track(self, times):
        self.wallet = self.init.fill_wallet(self.wallet)
        data = self.exchange.ticker()

        if times % 10 == 0:
            print(f'Times: {times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO][globalvar.DEFAULT_CURRENCIES[0]]):.2f}')

        loop = asyncio.get_event_loop()
        for crypto in self.wallet.keys():
            if crypto in globalvar.DEFAULT_CURRENCIES:
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
