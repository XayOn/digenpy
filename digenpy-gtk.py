#!/usr/bin/env python
"""
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
from digenpy import *
import sys, digenpy, types, pygtk, gtk, gtk.glade

class BasicDicts:
    def __init__(self):
        self.z=[]

    def generate(self, countrybox, companybox, fo, bssid, essid):
        module=getattr(digenpy, countrybox.get_model()[countrybox.get_active()][0])
        [self.z.append(getattr(module, companybox.get_model()[companybox.get_active()][0])) for a in dir(module)\
            if isinstance(getattr(module, a, None), types.ClassType) and a in sys.argv[2].split(',') ]
        [self.printer(fo, i(bssid, essid).dictionary) for i in self.z]

    def printer(fo, a_print):
        for a in a_print: fo.write(a)

class MainGUI:
    def __init__(self):
        self.dicts=BasicDicts()

        self.builder=gtk.Builder()
        self.builder.add_from_file('digenpy-gtk.glade')
        self.widgets=self.builder
        self.window=self.builder.get_object('MainWindow')

        self.widgets.connect_signals({
                'on_button_ok_clicked': self.generate,
                'on_button_cancel_clicked': gtk.main_quit,
                })

        self.countrybox=self.widgets.get_object('countrybox')
        self.companybox=self.widgets.get_object('companybox')
        self.countrybox.set_active(0)
        self.companybox.set_active(0)

    def generate(self, widgets):
        bssid=self.widgets.get_object('bssid').get_text()
        essid=self.widgets.get_object('essid').get_text()
        file_=self.widgets.get_object('file').get_text()
        self.dicts.generate(self.countrybox, self.companybox, open(file_), bssid, essid)

if __name__== "__main__":
    MainGUI()
    gtk.main()
