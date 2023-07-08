import json
import globalvar


class Store:
    def __init__(self):
        self.save_data = [{'option': globalvar.CURRENT_OPTION}]

    def save(self, wallet):
        for crypto in wallet.keys():
            if crypto == globalvar.DEFAULT_CURRENCY:
                continue
            if globalvar.CURRENT_OPTION == globalvar.OPTION_STEPS:
                difference = f'{float( wallet[crypto].rate) - float(wallet[crypto].buy_rate):.8f}'
                if '.' in difference:
                    difference = difference.rstrip('0').rstrip('.')

                crypto_data = {
                    'code': wallet[crypto].code,
                    'rate': wallet[crypto].rate,
                    'last_rate': wallet[crypto].last_rate,
                    'top_rate': wallet[crypto].top_rate,
                    'buy_rate': wallet[crypto].buy_rate,
                    'amount': wallet[crypto].amount,
                    'amount_€': float(wallet[crypto].rate) * float(wallet[crypto].amount),
                    'position': wallet[crypto].position,
                    # 'more_⇧': wallet[crypto].more,
                    # 'less_⇩': wallet[crypto].less,
                    'sells': wallet[crypto].sells,
                    'difference': difference,
                    'profit': wallet[crypto].profit,
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
            self.save_data.append(crypto_data)

        dump = json.dumps(self.save_data)
        with open(globalvar.SAVE_FILE, 'w') as file:
            file.write(dump)
            self.save_data = []
            file.close()
            return
