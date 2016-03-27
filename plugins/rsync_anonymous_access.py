# -*- coding:utf8 -*-
__author__ = 'newbie0086#foxmail.com'
import os
import platform
import subprocess
import signal
import time
import re


class TimeoutError(Exception):
    pass

def command(cmd, timeout):
    is_linux = platform.system() == 'Linux'
    try:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid if is_linux else None)
    except Exception,e:
        pass
    t_beginning = time.time()

    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            if is_linux:
                os.killpg(p.pid, signal.SIGTERM)
            else:
                p.terminate()
            raise TimeoutError(cmd, timeout)
        time.sleep(0.1)
    return p.stdout.read()

def check(host,port,timeout):
    try:
        cmd="rsync %s::"%host
        results= command(cmd,timeout)
        if 'rsync' in results:
            info="rsync %s:: \t return information success!!!"%host
            return 'YES|'+info

        #print results
        #matchfaild=re.search(r'Receiver=3.0.9',results)




    except Exception,e:
        return 'NO'
    return 'NO'
