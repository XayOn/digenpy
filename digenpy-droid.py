#!/usr/bin/env python
"""
 Copyright (C) 2011 David Francos Cuartero
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
from Digenpy_ import *
import sys, Digenpy_, types, android
from gettext import gettext as _

class MainGUI:
    def __init__(self):
        self.droid=android.Android()
        sys.excepthook = self.exception_handler
        self.generate()

    def _generate(self, country, company, fo, bssid, essid):
        return self.printer(fo, getattr( getattr(Digenpy_, country),
            company)(['gui', bssid, essid]).dictionary)

    def printer(self, fo, a_print):
        return [ fo.write(a + '\n') for a in a_print ]

    def exception_handler(self, type_, value, traceback):
        self.droid.dialogCreateAlert(value.__str__())
        self.droid.dialogShow()

    def generate(self):
        self.droid.dialogCreateAlert('Country', 'Select country')
        self.droid.dialogSetItems(Digenpy_.__all__)
        self.droid.dialogShow()
        result=self.droid.dialogGetResponse().result['item']
        self.country=Digenpy_.__all__[result]
        print self.country
        mod=getattr(Digenpy_, self.country)
        self.companies=[ a for a in dir(mod) if isinstance(getattr(mod, a, None),
            types.ClassType) and getattr(mod, a)('').dictionary ]

        self.droid.dialogCreateAlert('Select company')
        self.droid.dialogSetItems(self.companies)

        self.droid.dialogShow()
        result=self.droid.dialogGetResponse().result['item']
        self.company=self.companies[result]

        bssid=self.droid.getInput('BSSID', 'Insert BSSID').result
        essid=self.droid.getInput('ESSID', 'Insert ESSID').result
        file_=self.droid.getInput('FILE', 'Insert destination file route (start it with /sdcard)').result

        if not bssid or not essid or not file_ or not self.company or not self.country:
            raise Exception(_('Error: Some of the needed data is missing\nMake sure you\'ve entered the bssid, essid and destfile, as well as company and country'))

        self._generate(self.country, self.company, open(file_,'a+'), bssid, essid)
        raise Exception(_('Dicts correctly generated in ') + file_)

if __name__ == "__main__":
    MainGUI()
    droid.exit()
