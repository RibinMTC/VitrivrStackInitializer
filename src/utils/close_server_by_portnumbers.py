import os
import subprocess
import re
from pathlib import Path


def get_pids(port):
    command = "lsof -i :%s | awk '{print $2}'" % port
    pids = subprocess.check_output(command, shell=True)
    pids = pids.strip()
    if pids:
        pids = re.sub(' +', ' ', pids)
        for pid in pids.split('\n'):
            try:
                yield int(pid)
            except:
                pass


def close_process_by_port(port):
    pids = set(get_pids(port))
    command = 'sudo kill -9 {}'.format(' '.join([str(pid) for pid in pids]))
    os.system(command)


vitrivr_ng_port = 4200
cineast_port = 4567
cottontail_port = 1865

d = str(Path().resolve().parent)
print(d)

close_process_by_port(vitrivr_ng_port)
