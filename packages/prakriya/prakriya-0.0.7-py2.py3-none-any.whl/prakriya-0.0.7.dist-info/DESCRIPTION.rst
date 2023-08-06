========
prakriya
========


.. image:: https://img.shields.io/pypi/v/prakriya.svg
        :target: https://pypi.python.org/pypi/prakriya

.. image:: https://img.shields.io/travis/drdhaval2785/python-prakriya.svg
        :target: https://travis-ci.org/drdhaval2785/python-prakriya

.. image:: https://readthedocs.org/projects/prakriya/badge/?version=latest
        :target: https://prakriya.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/drdhaval2785/python-prakriya/shield.svg
     :target: https://pyup.io/repos/github/drdhaval2785/python-prakriya/
     :alt: Updates

.. image:: https://landscape.io/github/drdhaval2785/python-prakriya/master/landscape.svg?style=flat
     :target: https://landscape.io/github/drdhaval2785/python-prakriya/master
     :alt: Code health

.. image:: https://coveralls.io/repos/github/drdhaval2785/python-prakriya/badge.svg?branch=master
     :target: https://coveralls.io/github/drdhaval2785/python-prakriya?branch=master
     :alt: Code coverage

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
     :target: https://www.paypal.me/drdhaval2785/500inr
     :alt: Paypal

prakriya is a package to derive information about given Sanskrit verb form.


* Free software: GNU General Public License v3
* Documentation: https://prakriya.readthedocs.io.


Features
--------

1. Provides step by step derivation based on Panini's grammar of Sanskrit.
2. Supports various transliteration as input and output.
3. Also provides a commandline tool.


Support
-------
1. You can help development of code by testing and bug report.
2. You can contribute monetarily at the following link.

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
     :target: https://www.paypal.me/drdhaval2785/500inr
     :alt: Paypal


Credits
---------

1. This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

2. This package uses indic-transliteration_ package.

.. _indic-transliteration: https://pypi.python.org/pypi/indic-transliteration


=======
History
=======

0.0.1 (2017-12-30)
------------------

* First release on PyPI.

0.0.2 (2018-01-01)
------------------

Broken release. Kindly update to v0.0.3 immediately.

0.0.3 (2018-01-02)
------------------

A fix for broken v0.0.2 release.
jsonindex.json file which was crucial and missed in v0.0.2, added back.

0.0.4 (2018-01-03)
------------------

1. Added transliteration support. See #5 .
2. Adding data file in system specific locations like APPDATA. See #6 .
3. Made code python 2.7, 3.3, 3.4, 3.5, 3.6 compliant.
4. Corrected all errors / smells identified by landscape.io.

0.0.5 (2018-01-13)
------------------

1. Added verb form generation facility. See https://github.com/drdhaval2785/prakriya/issues/39.

0.0.6 (2018-10-16)
------------------

1. Added CLI functionality 'generate'. See https://github.com/drdhaval2785/python-prakriya/issues/12.
2. Guess the correct verb e.g. eD -> eDa~. See https://github.com/drdhaval2785/python-prakriya/issues/13.
3. All data files moved to appdata folder. See https://github.com/drdhaval2785/python-prakriya/issues/14.
4. Memoize data read from JSONs for speedup. See https://github.com/drdhaval2785/python-prakriya/issues/15.
5. Removed unnecessary duplicate loading of JSONs. See https://github.com/drdhaval2785/python-prakriya/issues/11.


