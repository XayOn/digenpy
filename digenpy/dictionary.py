#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Dictionary(object):
    def __init__(self, caller, cls):
        self.caller = caller
        self.parser = caller.subparsers[cls.__module__][cls.__class__.__name__]
