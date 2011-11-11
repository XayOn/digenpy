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
import sys, string, hashlib, android, random, logging

class DigenpyAndroid(object):

    def __init__(self):
        logging.info("Starting script, getting API, interface is\
                digenpy_interface.html by default at /sdcard for tests")
        self.droid=android.Android()
        self.webviewfile="auto.html"
        self.generate_interface('/sdcard/digenpy_interface.html')

    def generate_interface(self, company):
        self.droid.webViewShow(self.webviewfile)
        self.droid.toggleWifiState(1)
        while True:
            self.data=self.droid.EventWaitfor('generate_dict').result
            self.publish_results()

    def get_requisites(self, company):
        c_reqs=getattr(self, company)()
        return [ self.data[i] for i in c_reqs ]

    def publish_results(self, company):
        """
            TODO: This right now is a fucking memory problem. It probably will fill your memory!
        """
        results=getattr(self, company)(*get_requisites(company)).dictionary
        if len(results) == 1:
            text="Use this password?"
            result=results[0]
        else:
            result=random.choice(result)
            text="This is randomly-picken from all the %s ones generated. Use it?" %(len(results))

        self.droid.dialogCreateAlert( "The password is: %s" %(result), text )
        self.droid.dialogSetPositiveButtonText('Copy to clipboard and go to settings')
        self.droid.dialogSetNegativeButtonText('Back')
        self.droid.dialogShow()
        result_dialog = self.droid.dialogGetResponse().result['wich']
        if result_dialog == "positive":
            self.droid.setClipboard(result)
        self.droid.dialogDismiss()

    class Dlink(object):
        def __init__(self, *args):
            if not len(args[0]) > 1:
                return ['bssid']
            self.sm=args[0][1].split(':')
            self.dicts=[]
            self.S2=self.hexa_minus_one(self.sm[-1][1])
            self.S1=""
            if self.sm[-1][1] is 0: self.S1=self.hexa_minus_one(self.sm[-1][0])
            if self.S1 is -1: self.S2, self.S1 = [0,0]
            self.static="%s%s%s%s" %(self.sm[4], self.sm[1], self.sm[2],self.sm[3])

        @property
        def dictionary(self):
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
                return ['year', 'fixed_data']
            self.year=args[0][1]
            self.dicts=[]
            self.fixed="IX1V" + args[0][2]
    
        @property
        def dictionary(self):
            [[[[[[ self.dicts.append("%s%s%s%s%s%s%s%s" %(self.fixed, self.year, a, b, c, d, e, f) ) for a in range(0,9)] for b in range(0,9)] for c in range(0,9)] for d in range(0,9)] for e in range(0,9)] for f in range(0,9)]
            return self.dicts

    class Jazztel():
        def __init__(self, *args):
            if not len(args[0]) > 1:
                return ['bssid', 'essid', 'type']
    
            if args[0][3] is "WPA":
                self.dictionary=JazztelAndTelefonicaWPA(args).dictionary
            else:
                self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], { '00:1A:2B' : ['Comtrend', 'E001D20'] } ).dictionary

    class Telefonica():
        def __init__(self, *args):
            if not len(args[0]) > 1:
                return [ 'bssid', 'essid', 'type']
    
            if args[0][3] is "WPA":
                self.dictionary=JazztelAndTelefonicaWPA(args).dictionary
            else:
                self.dictionary=JazztelAndTelefonica(args[0][1], args[0][2], {
                    "00:60:B3": ["Z-com", "Z001349"],
                    "00:01:38": ["Xavi 7768r", "X000138"] ,
                    "00:03:C9": ["Comtrend 535", "C0030DA"],
                    "00:A0:C5": [ "Zyxel 650HW/660HW", "Z001349"],
                    "00:16:38": [ "Comtrend_536+", "C0030DA"],
                    "00:13:49": [ "P-660HW-D1", "Z001349", "Z0002CF" ] }).dictionary

class JazztelAndTelefonicaWPA():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            return [ 'bssid', 'essid']
        self.mac=args[0].replace(':','')
        self.essid=args[0].split("_")[1]
        self.static="bcgbghgg"

    @property
    def dictionary(self):
        return [hashlib.md5(self.static + self.mac[:-4] + self.essid + self.mac).hexdigest()[:-12], ]

class JazztelAndTelefonica():
    def __init__(self, *args):
        if not len(args[0]) > 1:
            return [ 'bssid', 'essid']
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


DigenpyAndroid()
