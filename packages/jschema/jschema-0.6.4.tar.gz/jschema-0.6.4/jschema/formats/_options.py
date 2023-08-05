# -*- coding: utf-8 -*-
import os

class Options(object):

    def __init__(self, options):
        self._dst = options["dst"]
        self._ns = options["ns"]

    @property
    def dst(self):
        return self._dst

    @property
    def ns(self):
        return self._ns
