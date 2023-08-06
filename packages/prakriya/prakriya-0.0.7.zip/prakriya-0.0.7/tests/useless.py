#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cProfile
import pstats
import sys
import os
import ujson
from prakriya import Generate, Prakriya


# from prakriya.utils import readJson
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

# Start profiling.
profileOn = True
if profileOn:
    pr = cProfile.Profile()
    pr.enable()


def gentest():
    from prakriya import Generate
    g = Generate()
    verbs = [member for member in g.verbmap]
    counter = 0
    for verb in verbs:
        counter += 1
        if counter < 10:
            print(counter)
            print(verb)
            for outtran in g.validtrans:
                g.outputTranslit(outtran)
                for tense in g.validtenses:
                    for purusha in g.validpurushas:
                        for vachana in g.validvachanas:
                            g[verb, tense, purusha, vachana]


gentest()


"""
p = Prakriya()
with open(os.path.join('testdata', 'Bavati.json'), 'r') as fin:
    superdata = ujson.loads(fin.read())
"""
def comparetranslit(verbform, inTran, outTran, arguments=''):
    global p
    p.inputTranslit(inTran)
    p.outputTranslit(outTran)
    calculated = p[verbform, arguments]
    wholedata = superdata[outTran]
    if arguments == '':
        assert(calculated == wholedata)
    else:
        result = [member[arguments] for member in wholedata]
        assert(calculated == result)

def test_bhavati():
    """Test something."""

    """
    for (verbform, inTran) in [('Bavati', 'slp1')]:
        for outTran in ['slp1']:
            for x in xrange(169):
    """
    for (verbform, inTran) in [('Bavati', 'slp1'), ('ഭവതി', 'malayalam'),
                               ('భవతి', 'telugu'), ('bhavati', 'iast'),
                               ('भवति', 'devanagari'), ('Bavawi', 'wx'),
                               ('ભવતિ', 'gujarati'), ('bhavati', 'itrans'),
                               ('ଭଵତି', 'oriya'), ('ಭವತಿ', 'kannada'),
                               ('bhavati', 'hk'), ('ভবতি', 'bengali'),
                               ('ਭਵਤਿ', 'gurmukhi')]:
        for outTran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'wx',
                        'bengali', 'gujarati', 'gurmukhi', 'kannada',
                        'malayalam', 'oriya', 'telugu']:
            print('Testing ' + inTran + ' ' + outTran)
            comparetranslit(verbform, inTran, outTran)
            comparetranslit(verbform, inTran, outTran, 'prakriya')
            comparetranslit(verbform, inTran, outTran, 'verb')
            comparetranslit(verbform, inTran, outTran, 'verbaccent')
            comparetranslit(verbform, inTran, outTran, 'lakara')
            comparetranslit(verbform, inTran, outTran, 'gana')
            comparetranslit(verbform, inTran, outTran, 'meaning')
            comparetranslit(verbform, inTran, outTran, 'number')
            comparetranslit(verbform, inTran, outTran, 'madhaviya')
            comparetranslit(verbform, inTran, outTran, 'kshiratarangini')
            comparetranslit(verbform, inTran, outTran, 'dhatupradipa')
            comparetranslit(verbform, inTran, outTran, 'jnu')
            comparetranslit(verbform, inTran, outTran, 'uohyd')
            comparetranslit(verbform, inTran, outTran, 'upasarga')
            comparetranslit(verbform, inTran, outTran, 'padadecider_id')
            comparetranslit(verbform, inTran, outTran, 'padadecider_sutra')
            comparetranslit(verbform, inTran, outTran, 'it_id')
            comparetranslit(verbform, inTran, outTran, 'it_status')
            comparetranslit(verbform, inTran, outTran, 'it_sutra')
            comparetranslit(verbform, inTran, outTran, 'purusha')
            comparetranslit(verbform, inTran, outTran, 'vachana')


def test_generate():
    """Test generation class."""
    g = Generate()
    assert(g['BU', 'law', 'praTama', 'eka'] == [u'Bavati', u'BAvayati', u'BAvayate'])
    assert(g['BU', 'law', 'praTama', 'dvi'] == [u'BavataH', u'BAvayataH', u'BAvayete'])
    assert(g['BU', 'law', 'praTama', 'bahu'] == [u'Bavanti', u'BAvayanti', u'BAvayante'])
    assert(g['BU', 'law', 'maDyama', 'eka'] == [u'Bavasi', u'BAvayasi', u'BAvayase'])
    assert(g['BU', 'law', 'maDyama', 'dvi'] == [u'BavaTaH', u'BAvayaTaH', u'BAvayeTe'])
    assert(g['BU', 'law', 'maDyama', 'bahu'] == [u'BavaTa', u'BAvayaTa', u'BAvayaDve'])
    assert(g['BU', 'law', 'uttama', 'eka'] == [u'BavAmi', u'BAvayAmi', u'BAvaye'])
    assert(g['BU', 'law', 'uttama', 'dvi'] == [u'BavAvaH', u'BAvayAvaH', u'BAvayAvahe'])
    assert(g['BU', 'law', 'uttama', 'bahu'] == [u'BavAmaH', u'BAvayAmaH', u'BAvayAmahe'])
    assert(g['BU', 'low', 'tip'] == [u'BAvayatu', u'BAvayatAt', u'Bavatu', u'BavatAt'])
    assert(g['BU', 'low', 'tas'] == [u'BAvayatAm', u'BavatAm'])
    assert(g['BU', 'low', 'Ji'] == [u'BAvayantu', u'Bavantu'])
    assert(g['BU', 'low', 'sip'] == [u'BAvaya', u'BAvayatAt', u'Bava', u'BavatAt'])
    assert(g['BU', 'low', 'Tas'] == [u'BAvayatam', u'Bavatam'])
    assert(g['BU', 'low', 'Ta'] == [u'BAvayata', u'Bavata'])
    assert(g['BU', 'low', 'mip'] == [u'BAvayAni', u'BavAni'])
    assert(g['BU', 'low', 'vas'] == [u'BAvayAva', u'BavAva'])
    assert(g['BU', 'low', 'mas'] == [u'BAvayAma', u'BavAma'])
    # Test for stripped verbs.
    assert(g['eD', 'low', 'Ja'] == [u'eDantAm'])
    g.inputTranslit('hk')
    g.outputTranslit('itrans')
    assert(g['bhU', 'laT', 'jhi'] == [u'bhavanti', u'bhAvayanti'])
    g.inputTranslit('devanagari')
    g.outputTranslit('iast')
    assert(g['भू', 'लट्', 'झि'] == [u'bhavanti', u'bh\u0101vayanti'])

# test_bhavati()
# test_generate()
if profileOn:
    # Print profile info.
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
