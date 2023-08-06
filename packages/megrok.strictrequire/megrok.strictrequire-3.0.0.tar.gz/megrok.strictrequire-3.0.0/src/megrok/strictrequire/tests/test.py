#############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
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

import doctest
import megrok.strictrequire.tests
import unittest
import zope.component.testlayer

from zope.testing import renormalizing


layer = zope.component.testlayer.ZCMLFileLayer(megrok.strictrequire.tests)

checker = renormalizing.RENormalizing()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        doctest.DocFileSuite(
            'checkrequire.txt',
            checker=checker,
            optionflags=(
                doctest.NORMALIZE_WHITESPACE +
                doctest.ELLIPSIS +
                renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2)))
    suite.layer = layer
    return suite
