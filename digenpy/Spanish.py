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
import sys, string

class Dlink():
    def __init__(self, *args):
        self.sm=args[0][1].split(':')
        self.dicts=[]
        self.S2=self.hexa_minus_one(self.sm[-1][1])
        if self.sm[-1][1] is 0: self.S1=self.hexa_minus_one(self.sm[-1][0])
        if self.S1 is -1: self.S2, self.S1 = [0,0]
        self.static=self.sm[5].self.sm[2]. self.sm[3].self.sm[4]

    @property
    def dictionary(self):
        for self.F in string.hexdigits.replace('abcdef',''):
            for self.I in string.hexdigits.replace('abcdef',''):
                self.dicts.append("%s%s%s%s%s%s%s%s%s%s\n%s%s%s%s%s%s%s%s%s%s\nz%s%s%s%s%s%s%s%s%s%s\n"\
                    %(self.sm[6], self.sm[1], self.static, self.sm[6], self.static, self.sm[1], self.F, self.I,
                        self.S1, self.S2, self.sm[1], self.static, self.sm[6], self.static, self.sm[1], self.F, self.I,
                        self.S1, self.S2, self.sm[1],self.static, self.S1, self.S2, self.sm[6],self.static,self.sm[1], self.F, self.I))
        return self.dicts

    def hexa_minus_one(self, hexa):
        if hex(int(hexa, 16) - 1).split('x')[0] == "-": return -1
        return hex(int(hexa, 16) - 1).split('x')[1]

class Tele2():
    def __init__(self, *args):
        self.year=args[0][1]
        self.dicts=[]
        self.fixed="IX1V" + args[0][2]

    @property
    def dictionary(self):
        [[[[[[ self.dicts.append("%s%s%s%s%s%s%s%s" %(self.fixed, self.year, a, b, c, d, e, f) ) for a in range(0,9)] for b in range(0,9)] for c in range(0,9)] for d in range(0,9)] for e in range(0,9)] for f in range(0,9)]
        return self.dicts

class Jazztel():
    def __init__(self, *args):
        self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], { '00:1A:2B' : ['Comtrend', 'E001D20'] } ).dictionary

class Telefonica():
    def __init__(self, *args):
        self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], {
            "00:60:B3": ["Z-com", "Z001349"],
            "00:01:38": ["Xavi 7768r", "X000138"] ,
            "00:03:C9": ["Comtrend 535", "C0030DA"],
            "00:A0:C5": [ "Zyxel 650HW/660HW", "Z001349"],
            "00:16:38": [ "Comtrend_536+", "C0030DA"],
            "00:13:49": [ "P-660HW-D1", "Z001349", "Z0002CF" ] }).dictionary

class JazztelAndTelefonica():
    def __init__(self, *args):
        self.sm=args[0].split(':')
        self.essid=args[1]
        self.dicts=[]
        self.valid_routers=args[2]

    @property
    def dictionary(self):
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
