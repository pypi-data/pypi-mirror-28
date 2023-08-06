#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python PWRCheck Reader Constants."""

import logging

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    ('%(asctime)s pwrcheck %(levelname)s %(name)s.%(funcName)s:%(lineno)d '
     ' - %(message)s'))

STREAM_ERRORS = ('raise', 'yield', 'ignore')

PWRCHECK_WARM_UP = 5

PWRCHECK_PROPERTIES = [
    'volts',
    'amps',
    'watts',
    'total_amp_hours',
    'forward_amp_hours',
    'reverse_amp_hours',
    'max_volts',
    'min_volts',
    'max_amps',
    'min_amps',
    'quality'
]
