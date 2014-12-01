import unittest
from Testing import ZopeTestCase as ztc

from Products.UWOshSuccess.tests.base import UWOshSuccessFunctionalTestCase
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ztc.FunctionalDocFileSuite(
                      'browser.txt', package='Products.UWOshSuccess.tests',
                      test_class=UWOshSuccessFunctionalTestCase))
    return suite
