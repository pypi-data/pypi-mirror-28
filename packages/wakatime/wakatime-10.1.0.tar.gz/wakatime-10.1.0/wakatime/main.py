# -*- coding: utf-8 -*-
"""
    wakatime.main
    ~~~~~~~~~~~~~

    Module entry point.

    :copyright: (c) 2013 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function

import logging
import os
import sys
import traceback

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(pwd))
sys.path.insert(0, os.path.join(pwd, 'packages'))

from .__about__ import __version__
from .api import send_heartbeats
from .arguments import parse_arguments
from .compat import u, json
from .constants import SUCCESS, UNKNOWN_ERROR
from .logger import setup_logging

log = logging.getLogger('WakaTime')

from .heartbeat import Heartbeat
from .offlinequeue import Queue


def execute(argv=None):
    if argv:
        sys.argv = ['wakatime'] + argv

    args, configs = parse_arguments()

    setup_logging(args, __version__)

    try:
        heartbeats = []

        hb = Heartbeat(vars(args), args, configs)
        if hb:
            heartbeats.append(hb)
        else:
            log.debug(hb.skip)

        if args.extra_heartbeats:
            try:
                for extra_data in json.loads(sys.stdin.readline()):
                    hb = Heartbeat(extra_data, args, configs)
                    if hb:
                        heartbeats.append(hb)
                    else:
                        log.debug(hb.skip)
            except json.JSONDecodeError as ex:
                log.warning(u('Malformed extra heartbeats json: {msg}').format(
                    msg=u(ex),
                ))

        retval = send_heartbeats(heartbeats, args, configs)
        if retval == SUCCESS:
            queue = Queue(args, configs)
            offline_heartbeats = queue.pop_many()
            if len(offline_heartbeats) > 0:
                retval = send_heartbeats(offline_heartbeats, args, configs)

        return retval

    except:
        log.traceback(logging.ERROR)
        print(traceback.format_exc())
        return UNKNOWN_ERROR
