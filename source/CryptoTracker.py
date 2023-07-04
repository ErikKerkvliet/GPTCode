from Crypto import Crypto
from Bitpanda import Bitpanda
from time import sleep
import globalvar
from Init import Init
from Store import Store


class CryptoPrices:
    def __init__(self):
        self.wallet = {}
        self.bitpanda = Bitpanda()
        self.init = Init(self.bitpanda)
        self.store = Store()
        self.times = 0

    def update_prices(self):
        data = self.bitpanda.ticker()

        if self.times % 10 == 0:
            print(f'Times: {self.times} | Rate BTC: {float(data[globalvar.DEFAULT_CRYPTO][globalvar.DEFAULT_CURRENCY]):.2f}')

        if self.times == 1:
            self.wallet = self.init.fill_wallet(self.wallet)

        for crypto in data.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue

            if crypto not in self.wallet.keys():
                self.wallet[crypto] = Crypto(crypto)
                self.wallet[crypto].rate = float(data[crypto][globalvar.DEFAULT_CURRENCY])
                self.wallet[crypto].set_rate(data[crypto])
                self.wallet[crypto].last_rate = self.wallet[crypto].rate

                if globalvar.TEST:
                    response = self.bitpanda.buy(self.wallet[crypto])
                    self.wallet[crypto].up(response)
                continue

            self.wallet[crypto].set_rate(data[crypto])

            buy_diff_perc = ((self.wallet[crypto].rate - self.wallet[crypto].buy_rate) / self.wallet[crypto].buy_rate)
            top_diff_perc = ((self.wallet[crypto].rate - self.wallet[crypto].top_rate) / self.wallet[crypto].top_rate)
            last_diff_perc = ((self.wallet[crypto].rate - self.wallet[crypto].last_rate) / self.wallet[crypto].last_rate)

            # if globalvar.TEST:
            #     self.bitpanda.sell(self.wallet[crypto])
            #     self.wallet[crypto].lower()
            #     self.wallet[crypto].print_variables()
            #     self.wallet[crypto].reset()
            #
            #     response = self.bitpanda.buy(self.wallet[crypto])
            #     self.wallet[crypto].up(response)
            #     continue

            if buy_diff_perc > globalvar.PROFIT_PERC:
                if self.wallet[crypto].value_drops >= globalvar.MAX_DROPS or top_diff_perc > globalvar.LOSS_PERC:
                    self.bitpanda.sell(self.wallet[crypto])
                    self.wallet[crypto].lower()
                    self.wallet[crypto].print_variables()
                    self.wallet[crypto].reset()

                    response = self.bitpanda.buy(self.wallet[crypto])
                    self.wallet[crypto].up(response)

            if last_diff_perc < 0:
                self.wallet[crypto].value_drops += 1
            elif last_diff_perc > 0:
                self.wallet[crypto].value_drops -= 1

            self.wallet[crypto].last_rate = self.wallet[crypto].rate
            self.store.save(self.wallet)

    def run_infinitely(self):
        while True:
            self.update_prices()
            self.times += 1
            sleep(globalvar.TIMER)


if __name__ == '__main__':
    cp = CryptoPrices()

    cp.run_infinitely()
