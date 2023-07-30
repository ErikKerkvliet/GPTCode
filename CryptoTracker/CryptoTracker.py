import globalvar
from time import sleep
from Store import Store
from Tracker import Tracker


class CryptoPrices:
    def __init__(self, glv):
        self.glv = glv

        self.store = Store(self.glv)
        self.resolver = self.glv.get_resolver(globalvar.RESOLVER)
        self.exchanges = [key for key, exchange in self.glv.exchanges.items() if exchange]
        self.tracker = Tracker(self.glv)
        self.crashes = {
            globalvar.EXCHANGES_BITPANDA: 0,
            globalvar.EXCHANGES_KRAKEN: 0,
        }

    def run_infinitely(self):
        print(f'Exchanges: {", ".join(self.exchanges)}')
        print(f'Option: {globalvar.RESOLVER}')
        print(f'Sleep time: {globalvar.SELL_TIMER}')
        print(f'Start time: {globalvar.start_time}\n--------------------')

        while True:
            with open("log.txt", "w") as log:
                # try:
                for tracker in self.exchanges:
                    self.glv.tracker = tracker
                    self.tracker.track()
                    self.store.save(self.tracker.wallet)
                    self.crashes[tracker] = 0
                # except Exception as e:
                #     print(f'Error occurred in: {self.glv.tracker}')
                #     self.crashes[tracker] > 1:
                #         del self.trackers[tracker]
                #     self.crashes[tracker] += 1
                #     traceback.print_exc(file=log)
                #     traceback.print_tb(e.__traceback__)
                #     continue
                self.glv.times += 1
                sleep(self.glv.timer)


if __name__ == '__main__':
    cp = CryptoPrices(globalvar.Globalvar())

    cp.run_infinitely()
