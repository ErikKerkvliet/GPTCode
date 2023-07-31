import json
import globalvar


class Store:
    def __init__(self, glv):
        self.glv = glv

        self.save_data = [{
            'resolver': globalvar.RESOLVER,
            'exchange': self.glv.tracker,
        }]

    def save(self, wallet):
        self.save_data[0] = {
            'run_time': globalvar.get_run_time(),
            'balance_euro': self.glv.balance_euro[self.glv.tracker]
        }
        for crypto in wallet.keys():
            if globalvar.RESOLVER == globalvar.RESOLVER_STEPS:
                difference = wallet[crypto].rate - wallet[crypto].buy_rate

                difference = f'{difference:.8f}'
                if '.' in difference:
                    difference = difference.rstrip('0').rstrip('.')

                amount = float(wallet[crypto].rate) * float(wallet[crypto].amount)
                rate = wallet[crypto].rate if wallet[crypto].rate > 1 else wallet[crypto].rate + 1
                buy_rate = wallet[crypto].buy_rate if wallet[crypto].buy_rate > 1 else wallet[crypto].buy_rate + 1

                difference_euro = (wallet[crypto].amount * rate) - (wallet[crypto].amount * buy_rate)

                crypto_data = {
                    'code': wallet[crypto].code,
                    'rate': wallet[crypto].rate,
                    'last_rate': wallet[crypto].last_rate,
                    'top_rate': wallet[crypto].top_rate,
                    'buy_rate': wallet[crypto].buy_rate,
                    'amount': wallet[crypto].amount,
                    'amount_€': wallet[crypto].amount_euro,
                    'position': wallet[crypto].position,
                    'drops': wallet[crypto].drops,
                    'difference': difference,
                    'difference_€': difference_euro,
                    'sells': wallet[crypto].sells,
                    'profit': wallet[crypto].profit,
                    'profit_€': wallet[crypto].profit_euro,
                }
            else:
                crypto_data = {
                    'code': wallet[crypto].code,
                    'rate': wallet[crypto].rate,
                    'buy_rate': wallet[crypto].buy_rate,
                    'top_rate': wallet[crypto].top_rate,
                    'last_rate': wallet[crypto].last_rate,
                    'drops': wallet[crypto].drops,
                    'amount_€': wallet[crypto].amount_euro,
                    'amount': wallet[crypto].amount,
                    'profit': wallet[crypto].profit,
                    'available': wallet[crypto].available,
                    'sells': wallet[crypto].sells,
                    'gain_€': wallet[crypto].gain,
                }
            self.save_data.append(crypto_data)

        dump = json.dumps(self.save_data)
        save_file = f'{globalvar.SAVE_FILE}_{self.glv.tracker}'
        with open(save_file, 'w') as file:
            file.write(dump)
            self.save_data = [{}]
            file.close()
            return
