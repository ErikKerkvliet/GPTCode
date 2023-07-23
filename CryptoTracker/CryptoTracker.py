import globalvar
from Trackers.BitpandaTracker import BitpandaTracker
from time import sleep
from Init import Init
from Store import Store
from Trackers.KrakenTracker import KrakenTracker


class CryptoPrices:
    def __init__(self):
        self.glv = globalvar.Globalvar()

        self.store = Store(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)
        self.trackers = {
            globalvar.EXCHANGES_BITPANDA: BitpandaTracker(self.glv),
            globalvar.EXCHANGES_KRAKEN: KrakenTracker(self.glv)
        }

    def run_infinitely(self):
        print(f'Exchanges: {", ".join([globalvar.EXCHANGES_BITPANDA, globalvar.EXCHANGES_KRAKEN])}')
        print(f'Option: {globalvar.RESOLVER}')
        print(f'Sleep time: {globalvar.TIMER}')
        print(f'Start time: {globalvar.start_time}\n--------------------')

        times = 0
        while True:
            # try:
            for tracker in [globalvar.EXCHANGES_BITPANDA, globalvar.EXCHANGES_KRAKEN]:
                self.trackers[tracker].track(times)
                self.store.save(self.trackers[tracker].wallet)
            # except:
            #     print(f'Error in {self.glv.tracker}')
            times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
