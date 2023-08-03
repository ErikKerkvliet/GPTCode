import subprocess
import os
import signal
import requests
from datetime import datetime

from Resolvers.Percentages import Percentages
from Resolvers.Profit import Profit
from Resolvers.Steps import Steps
from Store import Store

TEST = True

STATE_DEVELOPMENT = 'development'
STATE_PRODUCTION = 'production'
STATE = STATE_DEVELOPMENT

EXCHANGES_BITPANDA = 'Bitpanda'
EXCHANGES_KRAKEN = 'Kraken'
EXCHANGES_ONE_TRADING = 'OneTrading'

RESOLVER_STEPS = 'steps'
RESOLVER_PERCENTAGES = 'percentages'
RESOLVER_PROFIT = 'profit'
RESOLVER = RESOLVER_STEPS

ORDER_SIDE_BUY = 'buy'
ORDER_SIDE_SELL = 'sell'

DEFAULT_CURRENCY = 'EUR'
DEFAULT_CRYPTO = 'BTC'
BUY_TIMER = 20
SELL_TIMER = 600
MAX_DROPS = 3
MIN_UPS = 3
PROFIT_PERC = 0.01
LOSS_PERC = 0.01
MARGIN = 0.99
SELL_MARGIN = 0.997
BUY_MARGIN = 1.002
BUY_AMOUNT = 15
SAVE_FILE = '../save'
IP_WORK = '145.131.206.197'
IP_HOME = '80.60.131.14'
IP_VPS = ''

start_time = datetime.now().time().strftime("%H:%M:%S")


class Globalvar:
    def __init__(self):
        self.ip = self.get_ip()
        self.tracker = None
        self.timer = SELL_TIMER
        self.times = 0
        self.store = Store(self)
        self.exchanges = {
            EXCHANGES_BITPANDA: True,
            EXCHANGES_KRAKEN: True,
            EXCHANGES_ONE_TRADING: False,
        }
        self.balance_euro = {
            EXCHANGES_BITPANDA: 0,
            EXCHANGES_KRAKEN: 0,
            EXCHANGES_ONE_TRADING: 0,
        }
        self.wallets = {
            EXCHANGES_BITPANDA: {},
            EXCHANGES_KRAKEN: {},
            EXCHANGES_ONE_TRADING: {},
        }
        self.resolvers = {
            RESOLVER_PERCENTAGES: Percentages(self),
            RESOLVER_STEPS: Steps(self),
            RESOLVER_PROFIT: Profit(self),
        }

    def get_exchange(self, exchange):
        return self.exchanges[exchange]

    def get_resolver(self, resolver):
        return self.resolvers[resolver]

    @staticmethod
    def get_ip():
        # data = {'ip': '80.60.131.14'}
        response = requests.get('https://api.ipify.org/?format=json')
        data = response.json()
        response.close()

        return data['ip']


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)

    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
        if 'close' in stdout_line or 'finished' in stdout_line:
            os.killpg(os.getpgid(popen.pid), signal.SIGTERM)

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def convert_to_value(value):
    if isinstance(value, str) and value.isdigit():
        return int(value)
    try:
        float_value = float(value)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        return str(value)


def get_run_time():
    now = datetime.now().time().strftime("%H:%M:%S")
    run_time = datetime.strptime(now, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")

    return f'🕑 {run_time}'
