import unittest
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName

from Products.UWOshSuccess.tests.base import UWOshSuccessFunctionalTestCase
from DateTime import DateTime


class TestReports(UWOshSuccessFunctionalTestCase):

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testReportTestsToday(self):
        self.browserLogin('test_user_1_')
        self.becomeStudent()
        self.browser.open(self.portal.absolute_url())
        self.browser.getLink('Add BlueSheet').click()
        self.browser.getControl(name='testDate_year').value = ['2009',]
        self.browser.getControl(name='testDate_month').value = ['12',]
        self.browser.getControl(name='testDate_day').value = ['11',]
        self.browser.getControl(name='testAccommodationsRequested:list').value = ['calculator']
        self.browser.getControl('Save').click()

        blueSheet = self.portal.bluesheets['john-doe-blue-sheet']
        blueSheet.setTestDate(str(DateTime()))
        blueSheet.setFacultyWillPickupTest(True)
        blueSheet.setFacultyWillDropOffTest(True)
        blueSheet.reindexObject()

        self.becomeStaffMember()        
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.doActionFor(blueSheet, 'submitToInstructor')
        workflowTool.doActionFor(blueSheet, 'submitToOffice')
        workflowTool.doActionFor(blueSheet, 'approveBlueSheet')

        self.browser.open(self.portal.absolute_url() + '/tests-today')
        self.assertTrue('<h1 class="documentFirstHeading">Tests Today:' in self.browser.contents)
        self.assertTrue('John Doe Blue Sheet' in self.browser.contents)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReports))
    return suite
