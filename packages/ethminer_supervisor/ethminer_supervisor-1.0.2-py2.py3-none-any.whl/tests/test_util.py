#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
import sys
import unittest
try:
    from unittest import patch
except ImportError:
    from mock import patch

from ethminer_supervisor import cli, util


EXAMPLE = ('Dec 1 22:33:44 miner1 ethminer[1]:   m  11:11:11|ethminer  '
           'Speed 1.00 Mh/s    gpu/0 0.50  gpu/1 0.50 [A44+0:R0+0:F0] Time: 00:01')


class TestSupervisor(unittest.TestCase):
    def test_parse_time(self):
        time = util.parse_time(EXAMPLE)
        self.assertEquals(1, time.day)
        self.assertEquals(22, time.hour)
        self.assertEquals(33, time.minute)

    def test_old_time(self):
        response = util.is_old_time(datetime(year=2017, month=12, day=1, second=1))
        self.assertEquals(True, response)

    def test_cli(self):
        testargs = ["ethminer_supervisor"]
        with patch.object(sys, 'argv', testargs):
            cli.main()
