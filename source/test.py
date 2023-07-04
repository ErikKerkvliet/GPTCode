# import json
# import subprocess
# import os
# import signal
# import sys
#
#
# def execute(cmd):
#     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)
#
#     for stdout_line in iter(popen.stdout.readline, ""):
#         yield stdout_line
#         if 'close' in stdout_line or 'finished' in stdout_line:
#             os.killpg(os.getpgid(popen.pid), signal.SIGTERM)
#
#     popen.stdout.close()
#     return_code = popen.wait()
#     if return_code:
#         raise subprocess.CalledProcessError(return_code, cmd)
#
# cmd = ['curl', '-X', 'GET', 'https://api.bitpanda.com/v1/wallets', '-H', 'X-API-KEY:dafae09f622692a2acb9671492bb9d31e2f562bacc3e31be8ab2fe175825df83b11cfff55ec35719fbe64905ef6f8b694ea72153d89571dea46a77ac33ce182b']
# while 1:
#     for path in execute(cmd):
#         json.loads(path)
#         print(json.loads(path)['data'][0]['type'], end="")
#         exit()
