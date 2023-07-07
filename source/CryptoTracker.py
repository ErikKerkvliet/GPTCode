from Options.Percentages import Percentages
from Options.Steps import Steps
from time import sleep
import globalvar
from globalvar import Globalvar
from Init import Init
from Store import Store
from bitpanda.enums import OrderSide


class CryptoPrices:
    def __init__(self):
        self.wallet = {}
        self.glv = Globalvar()
        self.init = Init(self.glv.bitpanda)
        self.store = Store()
        self.times = 0
        self.options = {
            globalvar.OPTION_PERCENTAGES: Percentages(self.glv),
            globalvar.OPTION_STEPS: Steps(self.glv),
        }

    def update_prices(self):
        data = self.glv.bitpanda.ticker()

        if self.times % 10 == 0:
            print(f'Times: {self.times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO][globalvar.DEFAULT_CURRENCY]):.2f}')

        if self.times == 0:
            self.wallet = self.init.fill_wallet(self.wallet)

        for crypto in self.wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue

            self.wallet[crypto].set_rate(data[crypto])

            result = self.options[globalvar.CURRENT_OPTION].calculate(self.wallet[crypto])
            if result == OrderSide.SELL.value:
                self.glv.bitpanda.sell(self.wallet[crypto])
                crypto.position = 0
                crypto.more = 0
                crypto.less = 0

                self.glv.bitpanda.buy(crypto)

            elif result == OrderSide.BUY.value:
                self.glv.bitpanda.buy(crypto)

        self.store.save(self.wallet)
        self.glv.bitpanda.instruments = {}

    def run_infinitely(self):
        while True:
            self.update_prices()
            self.times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
