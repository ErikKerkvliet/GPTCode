import globalvar
from Bitpanda import Bitpanda
from Fill import Fill
from Kraken import Kraken
from OneTrading import OneTrading


class Tracker:
    def __init__(self, glv):
        self.glv = glv
        self.wallet = None
        self.fill = Fill(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)
        self.balance_euro = 0

        self.exchanges = {
            globalvar.EXCHANGES_BITPANDA: Bitpanda(self.glv),
            globalvar.EXCHANGES_KRAKEN: Kraken(self.glv),
            globalvar.EXCHANGES_ONE_TRADING: OneTrading(self.glv),
        }

    def track(self) -> None:
        self.wallet = self.fill.fill_wallet(self.exchanges[self.glv.tracker])
        self.wallet = self.exchanges[self.glv.tracker].ticker(self.wallet)
        for code in self.wallet.keys():
            if self.resolver.resolve_sell(self.wallet[code]):
                self.exchanges[self.glv.tracker].start_transaction(self.wallet[code], globalvar.ORDER_SIDE_SELL)

            if self.resolver.resolve_buy(self.wallet[code]):
                self.exchanges[self.glv.tracker].start_transaction(self.wallet[code], globalvar.ORDER_SIDE_BUY)

        self.glv.store.save(self.wallet)
