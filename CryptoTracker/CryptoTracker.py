import globalvar
from BitpandaTracker import BitpandaTracker
from time import sleep
from Init import Init
from Store import Store
from packages.bitpanda.enums import OrderSide
from KrakenTracker import KrakenTracker
import asyncio


class CryptoPrices:
    def __init__(self):
        self.glv = globalvar.Globalvar()
        self.wallet = self.glv.get_wallet()
        self.init = Init(self.glv)

        self.store = Store(self.glv)
        self.times = 0
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)
        self.kraken_tracker = KrakenTracker(self.glv)
        self.bitpanda_tracker = BitpandaTracker(self.glv)
        self.option = self.glv.get_option()

    def run_infinitely(self):
        print(f'Exchange: {globalvar.EXCHANGE}')
        print(f'Option: {globalvar.OPTION}')
        print(f'Sleep time: {globalvar.TIMER}')
        print(f'Start time: {globalvar.start_time}\n--------------------')

        while True:
            if globalvar.EXCHANGE == globalvar.EXCHANGES_BITPANDA:
                self.bitpanda_tracker.track(self.times)
            elif globalvar.EXCHANGE == globalvar.EXCHANGES_KRAKEN:
                self.kraken_tracker.track(self.times)
            self.store.save()
            self.times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
