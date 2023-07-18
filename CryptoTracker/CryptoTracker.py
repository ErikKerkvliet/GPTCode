import globalvar
from Options.Percentages import Percentages
from Options.Steps import Steps
from Options.Profit import Profit
from time import sleep
from Init import Init
from Store import Store
from packages.bitpanda.enums import OrderSide
import asyncio


class CryptoPrices:
    def __init__(self):
        self.glv = globalvar.Globalvar()
        self.wallet = self.glv.get_wallet()
        self.init = Init(self.glv)

        self.store = Store(self.glv)
        self.times = 0
        self.options = {
            globalvar.OPTION_PERCENTAGES: Percentages(self.glv),
            globalvar.OPTION_STEPS: Steps(self.glv),
            globalvar.OPTION_PROFIT: Profit(self.glv),
        }
        self.exchange = self.glv.get_exchange(globalvar.EXCHANGE)
        self.exchange.get_wallet()
        exit()

    def update_prices(self):

        self.init.fill_wallet()

        data = self.exchange.ticker()

        if self.times % 10 == 0:
            print(f'Times: {self.times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO][globalvar.DEFAULT_CURRENCY]):.2f}')

        loop = asyncio.get_event_loop()
        for crypto in self.wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue

            self.wallet[crypto].set_rate(data[crypto])

            result = self.options[globalvar.CURRENT_OPTION].calculate(self.wallet[crypto])
            if result == OrderSide.SELL.value:
                loop.run_until_complete(self.exchange.sell(self.wallet[crypto]))

                loop.run_until_complete(self.exchange.buy(self.wallet[crypto], 15))

            elif result == OrderSide.BUY.value:
                loop.run_until_complete(self.exchange.buy(self.wallet[crypto]))

        loop.run_until_complete(self.exchange.close_client())

        self.store.save()
        self.exchange.instruments = {}

    def run_infinitely(self):
        while True:
            self.update_prices()
            self.times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
