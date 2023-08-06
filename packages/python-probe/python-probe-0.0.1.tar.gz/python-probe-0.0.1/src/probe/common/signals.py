#!/usr/bin/env python
#
# Author: YankunLi <lioveni99@gmail.com>
# Date  :   2018.1.18

CEPH_GIT_NICE_VER = "0.94.*"

import os
import sys
import time
import signal

from probe.common.exception import SIGALRMException
from probe.common.exception import SIGHUPException

def signal_to_exception(signum, frame):
    """convert signal to exception"""
    if signum == signal.SIGALRM:
        raise SIGALRMException()
    if signum == signal.SIGHUP:
        raise SIGHUPException()
    raise SIGNALException(signum)

if __name__ == '__main__':
    pass


