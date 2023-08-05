#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2018-01-10
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

import os
import sys
import daemonize

BASE_PATH = "/tmp/angel/web"

HELP = """
This executable script is used to start/stop a angel_web process as a daemon process.
This requires specifying a pid file which is used to interact with the process.
Usage examples:
    {0} start
    {0} stop
    {0} restart
    {0} status
    {0} help
\n
"""

pidfile = os.path.join(BASE_PATH, ".pid")
stdout = os.path.join(BASE_PATH, "start.out")
stderr = os.path.join(BASE_PATH, "start.err")

def serve():
    from angel_web import app
    app.serve_forever()

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("command error, more information:" + HELP)
        exit(1)
    if not os.path.isdir(BASE_PATH):
        os.makedirs(BASE_PATH)
    action = sys.argv[1]
    if action == "start":
        daemonize.start(serve, pidfile, stdout=stdout, stderr=stderr)
    elif action == "stop":
        daemonize.stop(pidfile)
    elif action == "status":
        daemonize.status(pidfile)
    elif action == "restart":
        daemonize.restart(serve, pidfile, stdout=stdout, stderr=stderr)
    elif action == "help":
        sys.stderr.write(HELP)
    else:
        sys.stderr.write("command error, more information:\n" + HELP)

if __name__ == "__main__":
    main()
