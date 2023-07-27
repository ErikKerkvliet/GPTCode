import asyncio

import globalvar
from Fill import Fill


class BitpandaTracker:
    def __init__(self, glv):
        self.glv = glv
        self.glv.tracker = globalvar.EXCHANGES_BITPANDA
        self.wallet = {}
        self.fill = Fill(self.glv)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGES_BITPANDA)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER_STEPS)
        self.balance_euro = 0

    def track(self, times):
        if times % 10 == 0:
            print(f'Bitpanda - times: {times}')

        self.glv.tracker = globalvar.EXCHANGES_BITPANDA
        if times % 25 == 0:
            self.wallet = self.fill.fill_wallet(self.wallet)
        data = self.exchange.ticker()

        loop = asyncio.get_event_loop()
        for crypto in self.wallet.keys():
            self.wallet[crypto].set_rate(data[crypto])

            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                loop.run_until_complete(self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_SELL))

                loop.run_until_complete(self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_BUY))

            elif result == globalvar.ORDER_SIDE_BUY:
                loop.run_until_complete(self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_BUY))

        # loop.run_until_complete(self.exchange.close_client())

        self.exchange.instruments = {}
