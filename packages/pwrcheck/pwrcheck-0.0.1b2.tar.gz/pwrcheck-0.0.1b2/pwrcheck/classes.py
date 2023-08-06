#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python PWRCheck Reader Class Definitions."""

import logging
import threading

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
        streamreader = StreamReader(self._serial_int)
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


class StreamReader(object):
    """
    Reads Lines from a stream.
    """

    def __init__(self, stream=None, errors='raise'):
        """
        `stream`:   file-like object to read from, can be omitted to
                    pass data to `next` manually.
                    must support `.readline()` which returns a string
        `errors`: behaviour when a parse error is encountered. can be one of:
            `'raise'` (default) raise an exception immediately
            `'yield'`           yield the ParseError as an element in the
                                stream, and continue reading at the next line
            `'ignore'`          completely ignore and suppress the error, and
                                continue reading at the next line
        """

        if errors not in pwrcheck.STREAM_ERRORS:
            raise ValueError(
                'errors must be one of {!r} (was: {!r})'.format(
                    pwrcheck.STREAM_ERRORS, errors))

        self.errors = errors
        self.stream = stream
        self.buffer = b''

    def next(self, data=None):
        """
        consume `data` (if given, or calls `stream.read()` if `stream` was
        given in the constructor) and yield a list of `NMEASentence` objects
        parsed from the stream (may be empty)
        """
        if data is None:
            if self.stream:
                data = self.stream.readline()
            else:
                return

        lines = (self.buffer + data).split(b'\n')
        self.buffer = lines.pop()

        for line in lines:
            try:
                yield line
            except pwrcheck.ParseError as exc:
                if self.errors == 'raise':
                    raise exc
                if self.errors == 'yield':
                    yield exc
                if self.errors == 'ignore':
                    pass
