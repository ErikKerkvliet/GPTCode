import traceback

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

    def run_infinitely(self):
        print(f'Exchanges: {", ".join(self.exchanges)}')
        print(f'Option: {globalvar.RESOLVER}')
        print(f'Sleep time: {globalvar.TIMER}')
        print(f'Start time: {globalvar.start_time}')

        while len(self.exchanges) > 0:
            with open("log.txt", "w") as log:
                try:
                    for tracker in self.exchanges:
                        print(f'================================= {tracker.capitalize()} run_time: {globalvar.get_run_time()} - times: {self.glv.times} =================================')

                        self.glv.tracker = tracker
                        self.tracker.track()
                        self.glv.crashes[tracker] = 0
                except Exception as e:
                    print(f'Error occurred in: {self.glv.tracker}')
                    if self.glv.crashes[self.glv.tracker] > 1:
                        del self.exchanges[self.glv.tracker]
                    self.glv.crashes[tracker] += 1
                    traceback.print_exc(file=log)
                    traceback.print_tb(e.__traceback__)
                    continue
                self.glv.times += 1

                if self.glv.times % 25 == 0:
                    self.tracker.exchanges[globalvar.EXCHANGES_BITPANDA].close_client()
                sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices(globalvar.Globalvar())

    cp.run_infinitely()
