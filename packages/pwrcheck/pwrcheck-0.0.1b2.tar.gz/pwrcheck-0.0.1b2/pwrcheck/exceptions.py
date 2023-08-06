#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python PWRCheck Reader Constants."""

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


class ParseError(ValueError):
    def __init__(self, message, data):
        super(ParseError, self).__init__((message, data))
