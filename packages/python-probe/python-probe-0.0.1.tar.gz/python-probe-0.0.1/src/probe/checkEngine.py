#!/usr/bin/env python
#
# Author: YankunLi <lioveni99@gmail.com>
# Date  :   2018.1.18

CEPH_GIT_NICE_VER = "0.94.*"

import os
import sys
import time
import math
import json
import signal
import subprocess
import random
import threading

from probe.common import sendemail
from probe.common.warning import BaseWarning
from probe.common.exception import SIGALRMException
from probe.common.exception import SIGHUPException
from probe.common.exception import MetricException
from probe.common.exception import PopenException
from probe.common.signals import signal_to_exception
from probe.common.log import WLOG

interval_time = 30

def match_policys_and_warn(commands):
    for cmd in commands:
        cmd.match_policys(warn=True)

def policy_process_metrics(metrics):
    warning_thread = threading.Thread(target=match_policys_and_warn,
                                      args=[metrics])
    warning_thread.setDaemon(True)
    warning_thread.start()

class CheckEngine(object):
    wait_max_time = 10
    class Sender(object):
        @staticmethod
        def send(command):
            try:
                child = subprocess.Popen(command.binary,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                command.child_handler = child
            except Exception:
                raise PopenException()

    def __init__(self, config, log, commands):
        self.cmds = commands
        self.config = config
        self.log = log

    def handle_commands(self):
        self.log.debug("CheckEnging handle commands")
        self._check()

    def send_command(self, cmd):
        try:
            self.log.debug("send command " + cmd.name)
            self.Sender.send(cmd)
        except PopenException:
            self.log.warn("Sender exception")
            pass #TODO warning

    def _format_result(self, cmd):
        try:
            self.log.debug("format result")
            cmd.format_result()
        except Exception:
            print("format result exception")

    def _fetch_subprocess_result(self, cmd):
        try:
            self.log.debug("fetch subprocess result")
            cmd.fetch_result()
        except PopenException:
            self.log.warn("fetch subprocess fail")
            pass #TODO warning
        except Exception:
            self.log.warn("communicate exception")
            pass #TODO warning

    def _check(self):
        for cmd in self.cmds:
            self.send_command(cmd)
        for cmd in self.cmds:
            self._fetch_subprocess_result(cmd)
            self._format_result(cmd)


    def start(self):
        interval_time = int(self.config["engine"]["interval_time"])
        if interval_time < 0 or interval_time is None:
            self.logger.log("interval time %d must more than zero" % interval_time)
            raise Exception("interval time must more than zero")
        next_window = math.floor(time.time()/interval_time) * interval_time

        stagger_offset = random.uniform(0, interval_time-1)
        max_time = int(max(interval_time - stagger_offset, 1))

        signal.signal(signal.SIGALRM, signal_to_exception)

        while(1):
            try:
                time_to_sleep = (next_window + stagger_offset) - time.time()
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
                elif time_to_sleep < 0:
                    next_window = time.time()

                next_window += interval_time

                signal.alarm(max_time + 1000)
                self.log.debug("loop one time")
                self.handle_commands()
                signal.alarm(0)
                self.log.debug("use policy to process result")
                policy_process_metrics(self.cmds)
            except Exception, e:
                import traceback
                msg = "Check Engine catch a exception: " + str(e)
                self.log.error(msg)
                self.log.error("traceback info: " + traceback.format_exc())
                WLOG.log(msg, warn=True)

    def warn(self, ):
        pass


if __name__ == '__main__':
    import cephCluster
    cc = cephCluster.CephClusterMetric()
    metrics = [cc,]
    server = CheckEngine(metrics)
    server.start()
    # sys.exit(main())


