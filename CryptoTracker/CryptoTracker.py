import globalvar
from Trackers.BitpandaTracker import BitpandaTracker
from time import sleep
from Init import Init
from Store import Store
from Trackers.KrakenTracker import KrakenTracker


class CryptoPrices:
    def __init__(self):
        self.glv = globalvar.Globalvar()
        self.init = Init(self.glv)
        self.wallet = {}

        self.store = Store(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)
        self.trackers = {
            globalvar.EXCHANGES_BITPANDA: BitpandaTracker(self.glv),
            globalvar.EXCHANGES_KRAKEN: KrakenTracker(self.glv)
        }

    def run_infinitely(self):
        print(f'Exchange: {globalvar.EXCHANGE}')
        print(f'Option: {globalvar.RESOLVER}')
        print(f'Sleep time: {globalvar.TIMER}')
        print(f'Start time: {globalvar.start_time}\n--------------------')

        times = 0
        while True:
            self.trackers[globalvar.EXCHANGE].track(times)
            self.store.save(self.trackers[globalvar.EXCHANGE].wallet)
            times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
