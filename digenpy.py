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
import sys, digenpy, types
z=[]
module=getattr(digenpy, sys.argv[1])
[z.append(getattr(module, sys.argv[2])) for a in dir(module)\
    if isinstance(getattr(module, a, None), types.ClassType) and a in sys.argv[2].split(',') ]
[i(sys.argv[2:]) for i in z]
