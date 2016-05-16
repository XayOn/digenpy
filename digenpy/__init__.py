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


class Dictionary(object):
    """ Base dictionary class """
    def __init__(self, caller, cls):
        self.caller = caller
        self.cls = cls

    @property
    def parser(self):
        """ Parser """
        cls = self.cls
        return self.caller.subparsers[cls.__module__][cls.__class__.__name__]


def extract_classes(module):
    """ Extracts all classes in a module """
    try:
        module = import_module(str(module))
        for class_ in inspect.getmembers(module, inspect.isclass):
            if class_[1].__module__.startswith('digenpy.countries'):
                yield class_[1]
    except RuntimeError:
        pass


class Digenpy(object):
    """ Main digenpy class """
    subparsers = defaultdict(dict)
    companies = defaultdict(dict)

    @property
    def countries(self):
        """ List of modules in countries package """
        modules = iter_modules(digenpy.countries.__path__)
        return ["digenpy.countries.{}".format(mod) for _, mod, _ in modules]

    @property
    def parser(self):
        """ Argument parser magic """
        parser = argparse.ArgumentParser(
            description='Digenpy, default router password generator')

        for country in self.countries:
            subparsers = parser.add_subparsers(help="Choose your country")
            country_parser = subparsers.add_parser(
                country, help="Companies in {}".format(country))

            subparser = country_parser.add_subparsers()

            for comp in extract_classes(country):
                # We parse each class and add a subparser for it.
                self.subparsers[country][comp.__name__] = subparser.add_parser(
                    comp.__name__)
                self.companies[country][comp.__name__] = comp(self)
        return parser

    def __init__(self):
        self.args = self.parser.parse_args()
        self.company = self.companies[sys.argv[1]][sys.argv[2]]


def main():
    """ Main """
    digenpy_ = Digenpy()
    digenpy_.company.run()
    for result in digenpy_.company.dictionary:
        print(result)


if __name__ == "__main__":
    main()
