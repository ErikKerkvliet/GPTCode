import globalvar
from Crypto import Crypto


class Steps:
    def __init__(self, glv):
        self.glv = glv

    def resolve_sell(self, crypto: Crypto) -> bool:
        if crypto.rate is not None:
            code = crypto.code if len(crypto.code) == 4 else f'{crypto.code} '
            difference = crypto.rate / crypto.buy_rate
            percentage = round((difference - 1), 5)
            amount = round(difference * globalvar.BUY_AMOUNT, 5)
            sell = '✓✓✓✓' if amount > globalvar.BUY_AMOUNT * 1.01 else '⤫'
            if percentage < 0:
                percentage_colored = f'\033[91m{percentage}\033[0m'
            elif percentage > 0:
                percentage_colored = f'\033[92m{percentage}\033[0m'
            else:
                percentage_colored = percentage

            print(f'Coin: {code}, Difference: {percentage_colored}%, Amount €: {amount}, Drops: {crypto.drops}, Sell: {sell}')

        if crypto.balance == 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return False
        profit = crypto.rate > crypto.last_rate
        self.edit_positions(crypto, profit)

        if not profit:
            if crypto.drops > 1 \
                    and crypto.buy_rate < crypto.rate * globalvar.MARGIN:

                print('SELL!!!!!!!!!!!!!!!!!!!', 1)
                return True

            if crypto.buy_rate < crypto.rate * globalvar.MARGIN \
                    and crypto.rate < crypto.last_rate * globalvar.SELL_MARGIN:

                print('SELL!!!!!!!!!!!!!!!!!!!', 2)
                return True
        return False

    @staticmethod
    def resolve_buy(crypto) -> bool:
        if crypto.balance != 0 or crypto.last_rate is None or crypto.rate == crypto.last_rate:
            return False
        if crypto.position > 2 \
                and crypto.sell_rate is not None \
                or crypto.sell_rate < crypto.rate * globalvar.BUY_MARGIN:
            return True
        return False

    @staticmethod
    def edit_positions(crypto: Crypto, profit: bool):
        if profit:
            if crypto.position < 0:
                crypto.position = 1
            else:
                crypto.position += 1

            if crypto.drops > 0:
                crypto.drops -= 1
        else:
            if crypto.position > 0:
                crypto.position = -1
            else:
                crypto.position -= 1

            if crypto.drops < 2:
                crypto.drops += 1
