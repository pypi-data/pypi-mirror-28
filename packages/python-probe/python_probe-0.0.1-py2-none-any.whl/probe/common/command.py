#!/usr/bin/env python

import copy
from exception import ArgvException

class Command(object):
    """Shell command instance"""
    def __init__(self, command):
        if type(command) is list:
            self.cmd = command
        else:
            raise ArgvException("The type of command is not list")

    def add_argv(self, argv=[]):
        self.cmd += argv

    @property
    def command(self):
        return self.cmd


class CommandFactory(object):
    """Generate a command"""
    binary_cmd = ['/usr/bin/ceph']

    @staticmethod
    def initFactory(cmd=None, format=None):
        if cmd:
            CommandFactory.binary_cmd = cmd

    @staticmethod
    def generateCommand(root_cmd=None, *args):
        if root_cmd:
            new_cmd = [root_cmd] + args
        else:
            new_cmd =  copy.copy(CommandFactory.binary_cmd) + args
        return Command(new_cmd)
