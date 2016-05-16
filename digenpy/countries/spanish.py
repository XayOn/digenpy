#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Spanish Dictionary Generators for WEP and WPA Networks library
"""

import string
import hashlib
from digenpy import Dictionary


class Dlink(Dictionary):
    """
        Just specify the bssid to generate passwords for.
    """
    def __init__(self, caller):
        super(self.__class__, self).__init__(caller, self)
        self.parser.add_argument('--bssid', type=str, required=True)

    def run(self):
        """ Run """
        def hexa_minus_one(hexa):
            sign, data = hex(int(hexa, 16) - 1).split('x')
            if sign == "-":
                return -1
            return data

        self.parts = self.caller.args.bssid.split(':')
        self.section_2 = hexa_minus_one(self.parts[-1][1])
        self.section_1 = ""

        if self.parts[-1][1] == 0:
            self.section_1 = hexa_minus_one(self.parts[-1][0])

        if self.section_1 == -1:
            self.section_1, self.section_2 = [0, 0]

        self.static_data = "{}{}{}{}".format(
            self.parts[4], self.parts[1], self.parts[2], self.parts[3]
        )

    @property
    def dictionary(self):
        for first in string.hexdigits.replace('abcdef', ''):
            for second in string.hexdigits.replace('abcdef', ''):
                end = "{}{}".format(first, second)
                yield "{}{}{}{}{}{}{}".format(
                    self.parts[5], self.parts[0], self.static_data,
                    self.parts[5], self.static_data, self.parts[1], end
                )

                yield "{}{}{}{}{}{}{}{}{}{}".format(
                    self.section_1, self.section_2, self.parts[0],
                    self.static_data, self.section_1, self.section_2,
                    self.parts[5], self.static_data, self.parts[0], end
                )

                yield "{}{}{}{}{}{}{}{}".format(
                    self.section_1, self.section_2, self.parts[0],
                    self.static_data, self.parts[5], self.static_data,
                    self.parts[1], end
                )


class Tele2(Dictionary):
    """
        Usage: Tele2 year True|False

        ::

            year: year of router emision. Try some.
            fixed:True|False: Wheter to use as fixed data IX1V or IX1V1V
    """

    def __init__(self, caller):
        super(self.__class__, self).__init__(caller, self)
        self.parser.add_argument('--year', type=str, required=True)
        self.parser.add_argument('--fixed', action="store_true", required=True)

    def run(self):
        self.year = self.caller.args.year
        fixed = ""
        if self.caller.args.fixed:
            fixed = "IV"
        self.fixed = "IX1V" + fixed

    @property
    def dictionary(self):
        def get_combinations(n):
            for i in range(int("9" * n)):
                yield str(i).zfill(n)

        for comb in get_combinations(6):
            yield "{}{}{}".format(self.fixed, self.year, comb)


class Jazztel(Dictionary):
    def __init__(self, caller):
        super(self.__class__, self).__init__(caller, self)
        self.parser.add_argument('--essid', type=str, required=True)
        self.parser.add_argument('--bssid', type=str, required=True)

    def run(self):
        self.parts = self.caller.args.bssid.split(':')
        self.essid = self.caller.args.essid
        self.start = ':'.join(self.parts[:3])

    @property
    def dictionary(self):
        for fixed_pos in range(1, len(self.static_dict[self.start])):
            for hexa in range(0x0000, 0xFFFF):
                yield "{}{}{}".format(
                    self.static_dict[self.start][fixed_pos],
                    hexa,
                    self.essid[-2],
                    self.essid[-1]
                )

    @property
    def static_dict(self):
        return {
            '00:1A:2B': ['Comtrend', 'E001D20']
        }


class Telefonica(Dictionary):
    def __init__(self, caller):
        super(self.__class__, self).__init__(caller, self)
        self.parser.add_argument('--essid', type=str, required=True)
        self.parser.add_argument('--bssid', type=str, required=True)

    def run(self):
        self.parts = self.caller.args.bssid.split(':')
        self.essid = self.caller.args.essid
        self.start = ':'.join(self.parts[:3])

    @property
    def dictionary(self):
        for fixed_pos in range(1, len(self.static_dict[self.start])):
            for hexa in range(0x0000, 0xFFFF):
                yield "{}{}{}".format(
                    self.static_dict[self.start][fixed_pos],
                    hexa,
                    self.essid[-2],
                    self.essid[-1]
                )

    @property
    def static_dict(self):
        return {
            "00:60:B3": ["Z-com", "Z001349"],
            "00:01:38": ["Xavi 7768r", "X000138"],
            "00:03:C9": ["Comtrend 535", "C0030DA"],
            "00:A0:C5": ["Zyxel 650HW/660HW", "Z001349"],
            "00:16:38": ["Comtrend_536+", "C0030DA"],
            "00:1A:2B": ["Comtrend 5361", "C001D20"],
            "00:02:CF": ["P-660HW-D1", "Z0002CF"],
            "00:23:F8": ["P-660HW-D1", "Z0023F8"],
            "40:4A:03": ["Zyxel p660", "Z404A03"],
            "50:67:F0": ["Zyxel", "Z5067F0"],
            "E0:91:53": ["Xavi 7968-Solos 4610RD/461x", "E0:91:53"],
            "00:1F:9F": ["Thomson 2009", "T5YF69A"],
            "00:18:03": ["Huawei echolife hg520v", "H4A60BA", "H538FBF"],
            "00:13:49": ["P-660HW-D1", "Z001349", "Z0002CF"]
        }


class JazztelAndTelefonicaWPA(Dictionary):
    def __init__(self, caller):
        super(self.__class__, self).__init__(caller, self)
        self.parser.add_argument('--essid', type=str, required=True)
        self.parser.add_argument('--bssid', type=str, required=True)

    def run(self):
        self.mac = self.caller.args.bssid.replace(':', '')
        self.essid = self.caller.args.essid.split('_')[1]
        self.statics = ["bcgbghgg"]

    @property
    def dictionary(self):
        for static in self.statics:
            yield hashlib.md5("{}{}{}{}".format(
                static,
                self.mac[:-4],
                self.essid,
                self.mac
            )).hexdigest()[:-12]
