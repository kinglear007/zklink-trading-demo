#!/usr/bin/env python
# encoding: utf-8


class ZklClient(object):
    def __init__(self, endpoint, timeout=30):
        self.zkl_endpoint = endpoint
        self.timeout = timeout
