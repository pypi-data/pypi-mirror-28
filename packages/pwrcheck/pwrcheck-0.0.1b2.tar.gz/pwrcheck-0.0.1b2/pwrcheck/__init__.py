#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python PWRCheck Reader.

"""
Python PWRCheck Reader.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2018 Greg Albrecht
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/pwrcheck>

"""

from .exceptions import ParseError  # NOQA

from .constants import (LOG_FORMAT, LOG_LEVEL, PWRCHECK_PROPERTIES,  # NOQA
                        PWRCHECK_WARM_UP, STREAM_ERRORS)

from .classes import SerialPoller  # NOQA

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'
