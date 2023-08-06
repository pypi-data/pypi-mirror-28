#!/usr/bin/env python

import sys
import six


class CephException(Exception):
    """Base Ceph Exception"""
    message = "An unknown exception occurred"

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            if kwargs:
                message = message % kwargs
        except Exception:
            raise

        self.msg = message
        super(CephException, self).__init__(message)

    def __unicode__(self):
        return six.text_type(self.msg)

class OSDDownException(CephException):
    message = "The status of some OSD service is DOWN"

class OSDOutException(CephException):
    message = "The status of some OSD service is OUT"

class MONDownException(CephException):
    message = "MON service is DOWN"

class SMTPException(CephException):
    message = "unknown exception about SMTP"

class CephCommandException(CephException):
    message = "Executing command of Ceph fails"

class ArgvException(CephException):
    message = "Arguments Exception"

class MetricException(CephException):
    message = "Metric Exception"

class PopenException(CephException):
    message = "subprocess exception"

class SOCKETException(CephException):
    message = "socket exception"
#signal exception

class SIGNALException(Exception):
    message = "An unknown exception occurred"

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            if kwargs:
                message = message % kwargs
        except Exception:
            raise

        self.msg = message
        super(CephException, self).__init__(message)

class SIGALRMException(SIGNALException):
    message = "Time out exception"

class SIGHUPException(SIGNALException):
    message = "SIGHUP exception"


