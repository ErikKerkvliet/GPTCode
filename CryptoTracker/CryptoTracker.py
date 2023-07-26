import globalvar
from Trackers.BitpandaTracker import BitpandaTracker
from time import sleep
from Store import Store
from Trackers.KrakenTracker import KrakenTracker
import traceback


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
        self.crashes = {
            globalvar.EXCHANGES_BITPANDA: 0,
            globalvar.EXCHANGES_KRAKEN: 0,
        }

    def run_infinitely(self):
        print(f'Exchanges: {", ".join([globalvar.EXCHANGES_BITPANDA, globalvar.EXCHANGES_KRAKEN])}')
        print(f'Option: {globalvar.RESOLVER}')
        print(f'Sleep time: {globalvar.TIMER}')
        print(f'Start time: {globalvar.start_time}\n--------------------')

        times = 0
        while True:
            with open("log.txt", "w") as log:
                # try:
                for tracker in [globalvar.EXCHANGES_KRAKEN, globalvar.EXCHANGES_BITPANDA]:
                    self.trackers[tracker].track(times)
                    self.store.save(self.trackers[tracker].wallet)
                    self.crashes[tracker] = 0
                # except Exception as e:
                #     print(f'Error occurred in: {self.glv.tracker}')
                #     self.crashes[tracker] > 1:
                #         del self.trackers[tracker]
                #     self.crashes[tracker] += 1
                #     traceback.print_exc(file=log)
                #     traceback.print_tb(e.__traceback__)
                #     continue
                times += 1
                sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
