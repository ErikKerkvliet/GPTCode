import asyncio

import globalvar
from Bitpanda import Bitpanda
from Fill import Fill


class BitpandaTracker:
    def __init__(self, glv):
        self.glv = glv
        self.glv.tracker = globalvar.EXCHANGES_BITPANDA
        self.wallet = {}
        self.exchange = Bitpanda(self)
        self.fill = Fill(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER_STEPS)
        self.balance_euro = 0

    def track(self):
        if self.glv.times % 10 == 0:
            print(f'Bitpanda - times: {self.glv.times}')

        self.glv.tracker = globalvar.EXCHANGES_BITPANDA
        if self.glv.times % 25 == 0:
            self.wallet = self.fill.fill_wallet(self.wallet)
            self.exchange.pairs = self.exchange.asset_pairs()

        self.wallet = self.exchange.ticker()
        for crypto in self.wallet.keys():
            result = self.resolver.resolve(self.wallet[crypto])
            if result == globalvar.ORDER_SIDE_SELL:
                self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_SELL)

                self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_BUY)
                self.glv.timer = globalvar.SELL_TIMER
            elif result == globalvar.ORDER_SIDE_BUY:
                self.exchange.start_transaction(self.wallet[crypto], globalvar.ORDER_SIDE_BUY)

        self.exchange.instruments = {}
