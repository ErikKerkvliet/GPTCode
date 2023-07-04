import json
import subprocess
import os
import signal

TEST = True
DEFAULT_CURRENCY = 'EUR'
DEFAULT_CRYPTO = 'BTC'
TIMER = 20
MAX_DROPS = 5
PROFIT_PERC = 0.05
LOSS_PERC = 0.05
SELL_PERC = 0.95
BITPANDA_PERC = 0.006
SAVE_FILE = './save'


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