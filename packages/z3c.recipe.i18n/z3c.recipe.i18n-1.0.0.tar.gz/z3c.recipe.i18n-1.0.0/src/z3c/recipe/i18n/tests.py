##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.testing import renormalizing
import doctest
import re
import unittest
import zc.buildout.testing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('zope.app.locales', test)
    zc.buildout.testing.install('zope.component', test)
    zc.buildout.testing.install('zope.configuration', test)
    zc.buildout.testing.install('zope.event', test)
    zc.buildout.testing.install('zope.i18nmessageid', test)
    zc.buildout.testing.install('zope.interface', test)
    zc.buildout.testing.install('zope.location', test)
    zc.buildout.testing.install('zope.proxy', test)
    zc.buildout.testing.install('zope.schema', test)
    zc.buildout.testing.install('zope.security', test)
    zc.buildout.testing.install('zope.tal', test)
    zc.buildout.testing.install_develop('z3c.recipe.i18n', test)


checker = renormalizing.RENormalizing([
    zc.buildout.testing.normalize_path,
    (re.compile(
    "Couldn't find index page for '[a-zA-Z0-9.]+' "
    "\(maybe misspelled\?\)"
    "\n"
    ), ''),
    (re.compile("""['"][^\n"']+z3c.recipe.i18n[^\n"']*['"],"""),
     "'/z3c.recipe.i18n',"),
    (re.compile('#![^\n]+\n'), ''),
    (re.compile('-\S+-py\d[.]\d(-\S+)?.egg'), '-pyN.N.egg',),
    # the following are for compatibility with Windows
    (re.compile('-  .*\.exe\n'), ''),
    (re.compile('-script.py'), ''),
    (re.compile(r'\\[\\]?'), '/'),
    (re.compile('outputDir'), 'outputdir'),
    ])


def test_suite():
    return unittest.TestSuite(
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker),
        )
