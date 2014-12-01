import unittest
from Testing import ZopeTestCase as ztc

from Products.UWOshSuccess.tests.base import UWOshSuccessTestCase


class TestManageVocabularies(UWOshSuccessTestCase):

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testOfficeStaffMemberCanAddVocabularyItems(self):
        self.becomeStaffMember()
        accommodationsVocab = self.portal.portal_vocabularies.UWOshSuccessAccommodations
        self.assertTrue(accommodationsVocab is not None)
        accommodationsVocab.invokeFactory('SimpleVocabularyTerm', 'testVocabTerm')
        testVocabTerm = accommodationsVocab.testVocabTerm
        self.assertTrue(testVocabTerm is not None)

    def testForAddVocabularyItemPortalTab(self):
        portal_tabs = self.portal.portal_actions.portal_tabs
        portal_tabs.add_vocabulary_items is not None

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestManageVocabularies))
    return suite
