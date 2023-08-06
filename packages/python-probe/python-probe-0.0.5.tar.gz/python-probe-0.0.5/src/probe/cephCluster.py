#!/usr/bin/env python
#
# Author: YankunLi <lioveni99@gmail.com>
# Date  :   2018.1.18

CEPH_GIT_NICE_VER = "0.94.*"

import os
import sys
import time
import argparse
import errno
import math
import json
import string
import signal
import subprocess
import random
import threading

from probe.common.warning import BaseWarning
from probe.common.exception import SIGALRMException
from probe.common.exception import SIGHUPException
from probe.common.exception import MetricException
from probe.common.signals import signal_to_exception
from probe.common.log import WLOG

# class CephClusterMetric(Metric):
class CephClusterMetric(BaseWarning):
    """Collector ceph cluster mon and osd map
    raw result:
{
    "health": {
        "health": {
            "health_services": [
                {
                    "mons": [
                        {
                            "name": "ceph-mon-180",
                            "kb_total": 98544244,
                            "kb_used": 8002676,
                            "kb_avail": 85529140,
                            "avail_percent": 86,
                            "last_updated": "2018-01-19 10:05:57.499884",
                            "store_stats": {
                                "bytes_total": 2531563740,
                                "bytes_sst": 37910709,
                                "bytes_log": 2031616,
                                "bytes_misc": 2491621415,
                                "last_updated": "0.000000"
                            },
                            "health": "HEALTH_OK"
                        },
                        {
                            "name": "ceph-mon-181",
                            "kb_total": 98544244,
                            "kb_used": 6316028,
                            "kb_avail": 87215788,
                            "avail_percent": 88,
                            "last_updated": "2018-01-19 10:05:49.624680",
                            "store_stats": {
                                "bytes_total": 2082742166,
                                "bytes_sst": 37811980,
                                "bytes_log": 983040,
                                "bytes_misc": 2043947146,
                                "last_updated": "0.000000"
                            },
                            "health": "HEALTH_OK"
                        },
                        {
                            "name": "ceph-mon-182",
                            "kb_total": 98544244,
                            "kb_used": 4587624,
                            "kb_avail": 88944192,
                            "avail_percent": 90,
                            "last_updated": "2018-01-19 10:05:06.368427",
                            "store_stats": {
                                "bytes_total": 889641291,
                                "bytes_sst": 35771931,
                                "bytes_log": 10420224,
                                "bytes_misc": 843449136,
                                "last_updated": "0.000000"
                            },
                            "health": "HEALTH_OK"
                        }
                    ]
                }
            ]
        },
        "timechecks": {
            "epoch": 330,
            "round": 20328,
            "round_status": "finished",
            "mons": [
                {
                    "name": "ceph-mon-180",
                    "skew": 0.000000,
                    "latency": 0.000000,
                    "health": "HEALTH_OK"
                },
                {
                    "name": "ceph-mon-181",
                    "skew": -0.001476,
                    "latency": 0.005125,
                    "health": "HEALTH_OK"
                },
                {
                    "name": "ceph-mon-182",
                    "skew": 0.000000,
                    "latency": 0.008533,
                    "health": "HEALTH_OK"
                }
            ]
        },
        "summary": [
            {
                "severity": "HEALTH_WARN",
                "summary": "noscrub,nodeep-scrub flag(s) set"
            }
        ],
        "overall_status": "HEALTH_WARN",
        "detail": []
    },
    "fsid": "07d6a06f-7eec-44bb-862e-09b21d177331",
    "election_epoch": 330,
    "quorum": [
        0,
        1,
        2
    ],
    "quorum_names": [
        "ceph-mon-180",
        "ceph-mon-181",
        "ceph-mon-182"
    ],
    "monmap": {
        "epoch": 3,
        "fsid": "07d6a06f-7eec-44bb-862e-09b21d177331",
        "modified": "2016-06-21 10:53:48.871925",
        "created": "2016-06-21 10:08:04.265318",
        "mons": [
            {
                "rank": 0,
                "name": "ceph-mon-180",
                "addr": "10.100.13.180:6789\/0"
            },
            {
                "rank": 1,
                "name": "ceph-mon-181",
                "addr": "10.100.13.181:6789\/0"
            },
            {
                "rank": 2,
                "name": "ceph-mon-182",
                "addr": "10.100.13.182:6789\/0"
            }
        ]
    },
    "osdmap": {
        "osdmap": {
            "epoch": 2700,
            "num_osds": 18,
            "num_up_osds": 18,
            "num_in_osds": 18,
            "full": false,
            "nearfull": false,
            "num_remapped_pgs": 0
        }
    },
    "pgmap": {
        "pgs_by_state": [
            {
                "state_name": "active+clean",
                "count": 1144
            }
        ],
        "version": 36902401,
        "num_pgs": 1144,
        "data_bytes": 12463117119974,
        "bytes_used": 24371757244416,
        "bytes_avail": 29412639178752,
        "bytes_total": 53784396423168,
        "read_bytes_sec": 4008007,
        "write_bytes_sec": 4610491,
        "op_per_sec": 1103
    },
    "mdsmap": {
        "epoch": 1,
        "up": 0,
        "in": 0,
        "max": 0,
        "by_rank": []
    }
}
new result:
{
    "monmap": {
        "quorum_names": [
            "ceph-mon-180",
            "ceph-mon-181",
            "ceph-mon-182"
        ],
        "monmap": {
            "epoch": 3,
            "fsid": "07d6a06f-7eec-44bb-862e-09b21d177331",
            "modified": "2016-06-21 10:53:48.871925",
            "created": "2016-06-21 10:08:04.265318",
            "mons": [
                {
                    "rank": 0,
                    "name": "ceph-mon-180",
                    "addr": "10.100.13.180:6789\/0"
                },
                {
                    "rank": 1,
                    "name": "ceph-mon-181",
                    "addr": "10.100.13.181:6789\/0"
                },
                {
                    "rank": 2,
                    "name": "ceph-mon-182",
                    "addr": "10.100.13.182:6789\/0"
                }
            ]
        }
    },
    "osdmap": {
        "epoch": 2700,
        "num_osds": 18,
        "num_up_osds": 18,
        "num_in_osds": 18,
        "full": false,
        "nearfull": false,
        "num_remapped_pgs": 0
    },
}


    """
    command = ['/usr/bin/python', '/usr/bin/ceph', '-s', '-f', 'json']
    def __init__(self, config, cmd=None):
        self.name = "CephClusterMetric"
        if cmd:
            binary = cmd
        else:
            binary = self.command
        self.binary = binary
        self.need_warn = False
        self.raw_out = None
        self.raw_err = None
        self.child_handler = None
        self.warning_times = 0
        self.warning_interval = 60
        self.new_result = {"ceph": {
            "mon":{
                "quorum": None,
                "monmap": None
                },
            "osd":{
                "osdmap": None
                }
            }
        }
        super(CephClusterMetric, self).__init__(config)

    def match_policys(self,warn=False):
        try:
            mon = self.new_result['ceph']['mon']
            osd = self.new_result['ceph']['osd']
            miss = len(mon['monmap']['mons']) - len(mon['quorum'])
            if miss != 0 and warn:
                msg = "There are %d monitor down" % miss
                self.warn(message=msg)
            miss_up = osd['osdmap']['num_osds'] - osd['osdmap']['num_up_osds']
            miss_in = osd['osdmap']['num_osds'] - osd['osdmap']['num_in_osds']
            if miss_up != 0 and warn:
                msg = "There are %d osd down" % miss_up
                self.warn(message=msg)
            if miss_in != 0 and warn:
                msg = "There are %d osd out" % miss_in
                self.warn(message=msg)
            if miss or miss_up or miss_in:
                self.need_warn = True
            elif self.need_warn:
                msg = "ceph cluster health is OK"
                self.warn(msg)
                self.need_warn = False
        except Exception:
            raise
            pass #TODO
            # import traceback
            # traceback.print_exc()

    def format_result(self):
        if self.raw_err:
            raise MetricException()
        if self.raw_out:
            try:
                self.new_result['ceph']['mon']['quorum'] = self.raw_out['quorum']
                self.new_result['ceph']['mon']['monmap'] = self.raw_out['monmap']
                self.new_result['ceph']['osd']['osdmap'] = self.raw_out['osdmap']['osdmap']
            except Exception, e:
                pass #TODO
                # import traceback
                # traceback.print_exc(str(e))

    @property
    def raw_out(self):
        return self._raw_out

    @raw_out.setter
    def raw_out(self, value):
        self._raw_out = value

    @property
    def raw_err(self):
        return self._raw_err

    @raw_err.setter
    def raw_err(self, value):
        self._raw_err = value

    def clean_all(self):
        self.need_warn = False
        self.raw_out = None
        self.raw_err = None
        self.child_handler = None
        self.new_result = None

    # def warn(self, message):
        # print(message)

    def fetch_result(self):
        try:
            result = self.child_handler.communicate()
        except Exception:
            raise
        if result[0]:
            self.raw_out = json.loads(result[0])
        if result[1]:
            self.raw_err = json.loads(result[1])

    def __str__(self):
        return self.__name__


if __name__ == '__main__':
    from checkEngine import CheckEngine
    cc = CephClusterMetric()
    metrics = [cc,]
    server = CheckEngine(metrics)
    server.start()
    # sys.exit(main())


