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
    Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA  02110-1301, USA.

"""
import sys
import inspect
import argparse
from pkgutil import iter_modules
from importlib import import_module
from collections import defaultdict
import digenpy.countries


def extract_classes(plugins):
    """
        Extracts all classes in
    """
    for module in plugins:
        try:
            module = import_module(str(module))
            for class_ in inspect.getmembers(module, inspect.isclass):
                if class_[1].__module__.startswith('digenpy.countries'):
                    yield class_[1]
        except RuntimeError:
            pass


class main(object):
    def __init__(self):
        self.subparsers = {}
        self.parser = argparse.ArgumentParser(
            description='Digenpy, default router password generator')

        modules = iter_modules(digenpy.countries.__path__)
        frmt = "digenpy.countries.{}"

        countries = [frmt.format(mod) for _, mod, _ in modules]
        companies = defaultdict(dict)

        subparsers = self.parser.add_subparsers(
            help="Choose your country")

        for country in countries:
            parser_country = subparsers.add_parser(
                country, help="Companies in {}".format(country))

            companies[country] = {}
            self.subparsers[country] = {}
            sparsers = parser_country.add_subparsers()

            for comp in extract_classes([country]):
                self.subparsers[country][comp.__name__] = sparsers.add_parser(
                    comp.__name__)
                companies[country][comp.__name__] = comp(self)

        self.args = self.parser.parse_args()
        comp = companies[sys.argv[1]][sys.argv[2]]
        comp.run()
        for r in comp.dictionary:
            print r


if __name__ == "__main__":
    main()
