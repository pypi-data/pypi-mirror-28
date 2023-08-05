#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cProfile
import pstats
import sys
from prakriya import Generate
from indic_transliteration import sanscript
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO
# Start profiling.
profileOn = True
if profileOn:
    pr = cProfile.Profile()
    pr.enable()

g = Generate()
g.inputTranslit('devanagari')
g.outputTranslit('iast')
print(g['भू', 'लट्', 'झि'])
"""
print(g['BU', 'low', 'tip'])
print(g['BU', 'low', 'tas'])
print(g['BU', 'low', 'Ji'])
print(g['BU', 'low', 'sip'])
print(g['BU', 'low', 'Tas'])
print(g['BU', 'low', 'Ta'])
print(g['BU', 'low', 'mip'])
print(g['BU', 'low', 'vas'])
print(g['BU', 'low', 'mas'])
"""
if profileOn:
    # Print profile info.
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
