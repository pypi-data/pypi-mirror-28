#!/usr/bin/env python

# Author: YankunLi
# Date:   20180122

import socket

from probe.common.sendemail import send_email
from probe.common.exception import SOCKETException

class BaseWarning(object):
    def __init__(self, config):
        if config["warning"]["header"]:
            self.header = config["warning"]["header"]
        else:
            self.header = None
        if config["warning"]["msg_body"]:
            self.msg = config["warning"]["msg_body"]
        else:
            self.msg = None

        if config["warning"]["emails"]:
            self.receivers = config["warning"]["emails"]
        else:
            self.receivers = ["liyankun160613@credithc.com", "cloud@credithc.com"]
        try:
            self.hostname = socket.gethostname()
            local_ip = socket.gethostbyname(self.hostname)
            if local_ip:
                self.ip = local_ip
            else:
                self.ip = "127.0.0.1"
        except Exception, e:
            raise SOCKETException("Get hostname fail")

    def warn(self, receivers=None, header=None, message=None, *args, **kwargs):
        if message:
            e_message = message
            if kwargs:
                e_message = message % kwargs
        else:
            e_message = self.msg

        if header:
            e_header = header
        else:
            e_header = self.header

        if receivers:
            e_receivers = receivers
        else:
            e_receivers = self.receivers

        e_header += ": " + self.ip

        send_email(e_receivers, e_header, e_message)
