#!/usr/bin/env python

# Author: YankunLi
# Date  : 20180122

import os
import sys

import argparse
import configobj
import signal
# try:
#     from setproctitle import setproctitle
# except ImportError:
#     setproctitle = None

# for path in [
#         "/".join(["/opt", "probe", "src"]),
#         os.path.abspath(os.path.join(os.path.dirname(__file__)))]:
#     if os.path.exists(path):
#         sys.path.insert(0, path)
from probe.common.log import setup_logging
from probe.cephCluster import CephClusterMetric
from probe.checkEngine import CheckEngine

def init_probe():
    try:
        # Initialize Options

        defaults = {
            'skip_pidfile': False,
        }

        if os.name == 'nt':
            defaults['skip_pidfile'] = True

        parser = argparse.ArgumentParser("Probe ceph cluster status")

        parser.add_argument("-c", "--configfile",
                            dest="configfile",
                            default="/etc/probe/probe.conf",
                            help="config file")

        parser.add_argument("-i", "--interval",
                            dest="interval",
                            type=int,
                            default=60,
                            help="loop interval time")

        parser.add_argument("-f", "--foreground",
                            dest="foreground",
                            default=False,
                            action="store_true",
                            help="run in foreground")

        parser.add_argument("-l", "--log-stdout",
                            dest="log_stdout",
                            default=False,
                            action="store_true",
                            help="log to stdout")

        parser.add_argument("-p", "--pidfile",
                            dest="pidfile",
                            default=None,
                            help="pid file")

        parser.add_argument("-v", "--version",
                            dest="version",
                            default=False,
                            action="store_true",
                            help="display the version and exit")

        parser.add_argument("--skip-pidfile",
                            dest="skip_pidfile",
                            default=defaults['skip_pidfile'],
                            action="store_true",
                            help="Skip creating PID file")

        parser.add_argument("--skip-fork",
                            dest="skip_fork",
                            default=False,
                            action="store_true",
                            help="Skip forking (damonizing) process")

        # Parse Command Line Args
        args = parser.parse_args()

        # sys.exit(0)
        if args.version:
            print "Diamond version 1.0"
            sys.exit(0)

        # Initialize Config
        args.configfile = os.path.abspath(args.configfile)
        if os.path.exists(args.configfile):
            config = configobj.ConfigObj(args.configfile)
        else:
            print >> sys.stderr, "ERROR: Config file: %s does not exist." % (
                args.configfile)
            parser.print_help(sys.stderr)
            sys.exit(1)


        # Initialize Logging
        log = setup_logging(args.configfile, args.log_stdout)

    # Pass the exit up stream rather then handle it as an general exception
    except SystemExit, e:
        raise SystemExit

    except Exception, e:
        import traceback
        sys.stderr.write("Unhandled exception: %s" % str(e))
        sys.stderr.write("traceback: %s" % traceback.format_exc())
        sys.exit(1)

    try:
        # DAEMONIZE MANAGEMENT
        if not args.skip_fork:
            # Detatch Process
            if not args.foreground:

                # Double fork to serverize process
                log.info('Detaching Process.')

                # Fork 1
                try:
                    pid = os.fork()
                    if pid > 0:
                        # Exit first paren
                        sys.exit(0)
                except OSError, e:
                    print >> sys.stderr, "Failed to fork process." % (e)
                    sys.exit(1)
                # Decouple from parent environmen
                os.setsid()
                os.umask(0o022)
                # Fork 2
                try:
                    pid = os.fork()
                    if pid > 0:
                        # Exit second paren
                        sys.exit(0)
                except OSError, e:
                    print >> sys.stderr, "Failed to fork process." % (e)
                    sys.exit(1)
                # Close file descriptors so that we can detach
                sys.stdout.close()
                sys.stderr.close()
                sys.stdin.close()
                os.close(0)
                os.close(1)
                os.close(2)
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')

        # PID MANAGEMENT
        if not args.skip_pidfile:
            # Finish Initialize PID file
            if not args.foreground:
                # Write pid file
                pid = str(os.getpid())
                try:
                    pf = file(args.pidfile, 'w+')
                except IOError, e:
                    log.error("Failed to write child PID file: %s" % (e))
                    sys.exit(1)
                pf.write("%s\n" % pid)
                pf.close()
                # Log
                log.debug("Wrote child PID file: %s" % (args.pidfile))

        #buid metrics and initialize checkEngine
        log.info('initialize checking engine.')
        metrics = []
        ccm = CephClusterMetric(config=config)
        metrics.insert(0, ccm)
        engine = CheckEngine(config=config, log=log, commands=metrics)

        def shutdown_handler(signum, frame):
            log.info("Signal Received: %d" % (signum))
            # Delete Pidfile
            if not args.skip_pidfile and os.path.exists(args.pidfile):
                os.remove(args.pidfile)
                # Log
                log.debug("Removed PID file: %s" % (args.pidfile))
            sys.exit(0)

        # Set the signal handlers
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

        #Start check engine
        log.info('Start checking engine.')
        engine.start()

    # Pass the exit up stream rather then handle it as an general exception
    except SystemExit, e:
        raise SystemExit

    except Exception, e:
        import traceback
        log.error("Unhandled exception: %s" % str(e))
        log.error("traceback: %s" % traceback.format_exc())
        sys.exit(1)



def main():
    init_probe()

if __name__ == "__main__":
    if setproctitle:
        setproctitle(os.path.basename(__file__))
    sys.exit(main())
