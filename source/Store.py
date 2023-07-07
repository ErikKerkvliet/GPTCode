import json
import globalvar


class Store:
    def __init__(self):
        self.save_data = []

    def save(self, wallet):
        for crypto in wallet.keys():
            if globalvar.get_ip() == globalvar.IP_WORK:
                crypto_data = {
                    'code': wallet[crypto].code,
                    'rate': wallet[crypto].rate,
                    'last_rate': wallet[crypto].last_rate,
                    'buy_rate': wallet[crypto].buy_rate,
                    'amount': wallet[crypto].amount,
                    'position': wallet[crypto].position,
                    'up_down_⇩': wallet[crypto].up_down,
                    'down_up_⇧': wallet[crypto].down_up,
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
