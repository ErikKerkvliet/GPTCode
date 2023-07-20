import json
import globalvar


class Store:
    def __init__(self, glv):
        self.glv = glv

        self.save_data = [{'resolver': globalvar.RESOLVER}]

    def save(self, wallet):
        for crypto in wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue
            if globalvar.RESOLVER == globalvar.RESOLVER_STEPS:
                difference = wallet[crypto].rate - wallet[crypto].buy_rate

                difference = f'{difference:.8f}'
                difference_percentage = f'{float(difference) / float(wallet[crypto].rate):.8f}'
                if '.' in difference:
                    difference = difference.rstrip('0').rstrip('.')

                if '.' in difference_percentage:
                    difference_percentage = difference_percentage.rstrip('0').rstrip('.')

                crypto_data = {
                    'code': wallet[crypto].code,
                    'rate': wallet[crypto].rate,
                    'last_rate': wallet[crypto].last_rate,
                    'top_rate': wallet[crypto].top_rate,
                    'buy_rate': wallet[crypto].buy_rate,
                    'amount': wallet[crypto].amount,
                    'amount_€': float(wallet[crypto].rate) * float(wallet[crypto].amount),
                    'position': wallet[crypto].position,
                    'difference': difference,
                    'difference_%': difference_percentage,
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
                    'drops': wallet[crypto].value_drops,
                    'amount_€': wallet[crypto].amount_euro,
                    'amount': wallet[crypto].amount,
                    'profit': wallet[crypto].profit,
                    'available': wallet[crypto].available,
                    'sells': wallet[crypto].sells,
                    'gain_€': wallet[crypto].gain,
                }
            self.save_data[0]['run_time'] = globalvar.get_run_time()
            self.save_data.append(crypto_data)

        dump = json.dumps(self.save_data)
        save_file = globalvar.SAVE_FILE if not globalvar.TEST else globalvar.SAVE_FILE_TEST
        with open(globalvar.SAVE_FILE, 'w') as file:
            file.write(dump)
            self.save_data = [{}]
            file.close()
            return
