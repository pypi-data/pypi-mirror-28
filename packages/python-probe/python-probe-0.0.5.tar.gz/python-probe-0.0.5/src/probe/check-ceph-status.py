#!/usr/bin/env python
#
# Author: YankunLi <lioveni99@gmail.com>
# Date  :   2018.1.18

CEPH_GIT_NICE_VER = "0.94.*"

import os
import sys
import platform
import time

MYPATH = os.path.abspath(__file__)
MYDIR = os.path.dirname(MYPATH)
DEVMODEMSG = '*** DEVELOPER MODE: setting PATH, PYTHONPATH and LD_LIBRARY_PATH ***'

sys.path.insert(0, MYDIR)

if MYDIR.endswith('src') and \
   os.path.exists(os.path.join(MYDIR, '.libs')) and \
   os.path.exists(os.path.join(MYDIR, 'pybind')):
    if platform.system() == 'Darwin':
        lib_path_var = "DYLD_LIBRARY_PATH"
    else:
        lib_path_var = "LD_LIBRARY_PATH"

    py_binary = os.environ.get("PYTHON", "python")
    MYLIBPATH = os.path.join(MYDIR, '.libs')
    execv_cmd = ['python']
    if 'CEPH_DBG' in os.environ:
        execv_cmd += ['-mpdb']
    if lib_path_var in os.environ:
        if MYLIBPATH not in os.environ[lib_path_var]:
            os.environ[lib_path_var] += ':' + MYLIBPATH
            print >> sys.stderr, DEVMODEMSG
            os.execvp(py_binary, execv_cmd + sys.argv)
    else:
        os.environ[lib_path_var] = MYLIBPATH
        print >> sys.stderr, DEVMODEMSG
        os.execvp(py_binary, execv_cmd + sys.argv)
    sys.path.insert(0, os.path.join(MYDIR, 'pybind'))
    if os.environ.has_key('PATH') and MYDIR not in os.environ['PATH']:
        os.environ['PATH'] += ':' + MYDIR

import argparse
import errno
import math
import json
import string
import signal
import socket
import struct
import subprocess
import random

import sendemail
from exception import SIGALRMException
from exception import SIGHUPException


def main():
    #1.parse arguements
    #2.init logging
    #3.entry deamon
    ################################################################

    #1.build command
    #2.initialize command
    ################ entry loop
    #3.execute command
    #4.fetch result of command
    #5.format cli result return new result
    #6.check new result, judge if need warning
    #7.warning

    try:
        child = subprocess.Popen(command + ['-s'] + ['-f','json'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = child.communicate()
    except Exception, e:
        import traceback
        traceback.print_exc("subprocesss.Popen fails" + str(e))
    try:
        if result[0]:
            jresult = json.loads(result[0])
            if len(jresult['quorum']) != len(jresult['monmap']['mons']):
                raise Exception
            summary_osdmap = jresult['osdmap']['osdmap']
            if summary_osdmap['num_up_osds'] != summary_osdmap['num_osds']:
                raise Exception
            if summary_osdmap['num_in_osds'] != summary_osdmap['num_osds']:
                raise Exception

            print(type(result))
            print(result)
            # sendemail.send_email('cloud@credithc.com', "test", "ceph status is OK")
        else:
            pass
    except Exception, e:
        import traceback
        traceback.print_exc()
        pass


if __name__ == '__main__':
    server = CheckEngine("testt")
    server.start()
    # sys.exit(main())


