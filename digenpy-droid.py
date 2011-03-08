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
import sys, Digenpy_, types, Android
from gettext import gettext as _

class MainGUI:
    def __init__(self):
        self.droid=android.Android()
        sys.excepthook = self.exception_handler
        self.country=self.get_country()
        self.company=self.get_company()
        self.generate()

    def get_companies(self, country):
        mod=getattr(Digenpy_, country)
        return [ a for a in dir(mod) if isinstance(getattr(mod, a, None),
            types.ClassType) and getattr(mod, a)('').dictionary ]

    def generate(self, country, company, fo, bssid, essid):
        return self.printer(fo, getattr( getattr(Digenpy_, country),
            company)(['gui', bssid, essid]).dictionary)

    def printer(self, fo, a_print):
        return [ fo.write(a + '\n') for a in a_print ]

    def exception_handler(self, type_, value, traceback):
        return self.droid.makeToast(value.__str__())

    def get_country(self):
        self.droid.dialogCreateAlert('Select country')
        self.droid.dialogSetItems(Digenpy_.__all__)
        self.droid.dialogShow()
        if result.has_key('item'):
            return Digenpy_.__all__[result['item']]
        else:
            return "Spanish"

    def get_company(self):
        companies=self.get_companies(self.country)
        self.droid.dialogCreateAlert('Select company')
        self.droid.dialogSetItems(companies)
        self.droid.dialogShow()
        if result.has_key('item'):
            return companies[result['item']]
        else:
            raise Exception('Wrong company')

    def generate(self):
        bssid=self.droid.getInput('BSSID', 'Insert BSSID')
        essid=self.droid.getInput('ESSID', 'Insert ESSID')
        file_=self.droid.getInput('FILE', 'Insert destination file route (start it with /sdcard)')

        if not bssid or not essid or not file_ or not self.company or not self.country:
            raise Exception(_('Error: Some of the needed data is missing\nMake sure you\'ve entered the bssid, essid and destfile, as well as company and country'))

        self.generate(self.country, self.company, open(file_,'a+'), bssid, essid)
        raise Exception(_('Dicts correctly generated in ') + file_)

if __name__ == "__main__":
    MainGUI()
