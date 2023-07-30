import globalvar
from Bitpanda import Bitpanda
from Fill import Fill
from Kraken import Kraken
from OneTrading import OneTrading


class Tracker:
    def __init__(self, glv):
        self.glv = glv
        self.wallet = {}
        self.fill = Fill(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)
        self.balance_euro = 0

        self.exchanges = {
            globalvar.EXCHANGES_BITPANDA: Bitpanda(self.glv),
            globalvar.EXCHANGES_KRAKEN: Kraken(self.glv),
            globalvar.EXCHANGES_ONE_TRADING: OneTrading(self.glv),
        }

    def track(self) -> None:
        if self.glv.times % 10 == 0:
            print(f'{self.glv.tracker.capitalize()} - times: {self.glv.times}')

        if self.glv.times % 25 == 0:
            self.wallet = self.fill.fill_wallet(self.wallet, self.exchanges[self.glv.tracker])
            self.exchanges[self.glv.tracker].pairs = self.exchanges[self.glv.tracker].asset_pairs()

        self.wallet = self.exchanges[self.glv.tracker].ticker(None, self.wallet)
        for code in self.wallet.keys():
            if self.resolver.resolve_sell(self.wallet[code]):
                self.exchanges[self.glv.tracker].start_transaction(self.wallet[code], globalvar.ORDER_SIDE_SELL)
                self.glv.timer = globalvar.BUY_TIMER

            if self.resolver.resolve_buy(self.wallet[code]):
                self.exchanges[self.glv.tracker].start_transaction(self.wallet[code], globalvar.ORDER_SIDE_BUY)
                self.glv.timer = globalvar.SELL_TIMER

        self.glv.store.save(self.wallet)
