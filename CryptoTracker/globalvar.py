import subprocess
import os
import signal
import requests
import Exchanges.Bitpanda as Bitpanda
import Exchanges.Kraken as Kraken
from datetime import datetime

TEST = True

STATE_DEVELOPMENT = 'development'
STATE_PRODUCTION = 'production'
STATE = STATE_DEVELOPMENT

DEFAULT_CURRENCY = 'EUR'
DEFAULT_CRYPTO = 'BTC'
TIMER = 10
MAX_DROPS = 3
MIN_UPS = 3
PROFIT_PERC = 0.01
LOSS_PERC = 0.01
BITPANDA_MARGIN = 0.996
BUY_AMOUNT = 15
SAVE_FILE = '../save'
SAVE_FILE_TEST = '../save_test'
IP_WORK = '145.131.206.197'
IP_HOME = '80.60.131.14'
IP_VPS = ''
OPTION_STEPS = 'steps'
OPTION_PERCENTAGES = 'percentages'
OPTION_PROFIT = 'profit'
CURRENT_OPTION = OPTION_STEPS

start_time = datetime.now().time().strftime("%H:%M:%S")


class Globalvar:
    def __init__(self):
        self.wallet = {}
        self.exchanges = {
            'bitpanda': Bitpanda.Bitpanda(self),
            'kraken': Kraken.Kraken(self),
        }

    def get_wallet(self):
        return self.wallet

    def get_exchange(self, exchange) -> Bitpanda:
        return self.exchanges[exchange]


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


def get_ip():
    response = requests.get('https://api.ipify.org/?format=json')
    data = response.json()

    return data['ip']


def get_run_time():
    now = datetime.now().time().strftime("%H:%M:%S")
    run_time = datetime.strptime(now, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")

    return f'🕑 {run_time}'
