#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python PWRCheck Reader Class Definitions."""

import logging
import threading

import pynmea2
import serial

import pwrcheck

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


class SerialPoller(threading.Thread):

    """Threadable Object for polling a Serial Device."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pwrcheck.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pwrcheck.LOG_LEVEL)
        _console_handler.setFormatter(pwrcheck.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, serial_port, serial_speed):
        threading.Thread.__init__(self)
        self._serial_port = serial_port
        self._serial_speed = serial_speed
        self._stopped = False

        self.pwrcheck_props = {}
        for prop in pwrcheck.PWRCHECK_PROPERTIES:
            self.pwrcheck_props[prop] = None

        self._serial_int = serial.Serial(
            self._serial_port, self._serial_speed, timeout=1)

    def stop(self):
        """
        Stop the thread at the next opportunity.
        """
        self._stopped = True
        return self._stopped

    def run(self):
        streamreader = pynmea2.NMEAStreamReader(self._serial_int)
        try:
            while not self._stopped:
                for msg in streamreader.next():
                    for prop in pwrcheck.PWRCHECK_PROPERTIES:
                        if getattr(msg, prop, None) is not None:
                            self.pwrcheck_props[prop] = getattr(msg, prop)
                            # self._logger.debug(
                            #    '%s=%s', prop, self.pwrcheck_props[prop])
        except StopIteration:
            pass
