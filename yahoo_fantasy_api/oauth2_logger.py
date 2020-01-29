#!/usr/bin/python

import logging
import yahoo_oauth


def cleanup():
    # Cleanup the logging in yahoo_oauth.  It creates a logger that writes to
    # stderr.  We are going to recreate the logger so that we can use a handler
    # that writes to our log file.
    logging.setLoggerClass(logging.Logger)
    yahoo_oauth.yahoo_oauth.logger = logging.getLogger('mod_yahoo_oauth')
    logging.getLogger('mod_yahoo_oauth').setLevel(logging.WARN)
