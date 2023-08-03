import subprocess
import os
import signal

TEST = True
DEFAULT_CURRENCY = 'EUR'
TIMER = 60
MARGIN = 0.9994
SAVE_FILE = '../save'

WATCHER_STEPS = 'steps'
WATCHER_PERCENTAGES = 'percentages'
CURRENT_WATCHER = WATCHER_STEPS

EXCHANGES_BITPANDA = 'Bitpanda'
EXCHANGES_KRAKEN = 'Kraken'
EXCHANGES = [EXCHANGES_KRAKEN, EXCHANGES_BITPANDA]


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
        float_value = float(value) if value is not None else 0.0
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        return str(value)
