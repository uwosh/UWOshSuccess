import unittest
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName

from Products.UWOshSuccess.tests.base import UWOshSuccessTestCase

from DateTime import DateTime


class TestBlueSheet(UWOshSuccessTestCase):

    testCourses = ['COMP SCI 331 - 001C - Programming Languages - Daniel Boone - booned@uwosh.edu',
                   'COMP SCI 342 - 001C - Software Engineering II - Kathy Jones - jonesk@uwosh.edu',
                   'COMP SCI 480 - 002C - Topics in Comp Sci - Robert Robertson - robertr@uwosh.edu',
                   'MATH 172 - 001C - Calculus II - Jane Heart - heartj@uwosh.edu',
                   'COMP SCI 446 - 002I - Com Sci Independent Study - George Sleeps - sleeps@uwosh.edu']

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testSetFullName(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.setFullName('John Doe')
        self.assertEqual(blueSheet.getFullName(), 'John Doe')
        self.assertEqual(blueSheet.Title(), 'John Doe Blue Sheet')
        
    def testGetStudentNameDefaultAsStaffMember(self):
        self.becomeStaffMember()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getStudentNameDefault(), '')
    
    def testGetStudentNameDefaultAsStudent(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getStudentNameDefault(), 'John Doe')

    def testGetStudentEmailDefaultAsStaffMember(self):
        self.becomeStaffMember()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getStudentEmailDefault(), '')
    
    def testGetStudentEmailDefaultAsStudent(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getStudentEmailDefault(), 'test_user_1_@uwosh.edu')

    def testGetListOfReaders(self):
        self.becomeStaffMember()
        blueSheet = self.createTestBlueSheet()
        self.addReadersToSite([('testReader1', 'Test Reader 1'), ('testReader2', 'Test Reader 2')])
        self.assertEqual(blueSheet.schema['testReaderAssigned'].vocabulary, '_getTestReadersVocabulary')
        self.assertEqual(blueSheet._getTestReadersVocabulary(),
                         [(' ', ' '), ('testReader1', 'Test Reader 1'), ('testReader2', 'Test Reader 2')])
        
        self.becomeReader()
        self.assertEqual(blueSheet._getTestReadersVocabulary(), [(' ', ' '), ('test_user_1_', 'John Doe')])
        blueSheet.setTestReaderAssigned('testReader2')
        self.assertEqual(blueSheet._getTestReadersVocabulary(), [('testReader2', 'Test Reader 2')])

    def testGetWSCourseNumberNameFacultyAsStaffMember(self):
        self.becomeStaffMember()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getEmail(), '')
        self.assertEqual(blueSheet.getWSCourseNumberNameFaculty(), [' ',])
        blueSheet.setEmail('test_user_1_@uwosh.edu')
        self.assertEqual(blueSheet.getWSCourseNumberNameFaculty(), self.testCourses)

    def testGetWSCourseNumberNameFacultyAsStudent(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        self.assertEqual(blueSheet.getWSCourseNumberNameFaculty(), self.testCourses)

    def testSetCourseNumberNameFaculty(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.setCourseNumberNameFaculty('COMP SCI 331 - 001C - Programming Languages - Daniel Boone - booned@uwosh.edu')
        self.assertEqual(blueSheet.getCourseNumberNameFaculty(), 'COMP SCI 331 - 001C - Programming Languages - Daniel Boone - booned@uwosh.edu')
        self.assertEqual(blueSheet.getFacultyName(), 'booned')
        self.assertEqual(blueSheet.getFacultyEmail(), 'booned@uwosh.edu')

    def testSetCourseNumberNameFacultyWithEmptyValue(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.setCourseNumberNameFaculty(' ')
        self.assertEqual(blueSheet.getCourseNumberNameFaculty(), ' ')
        self.assertEqual(blueSheet.getFacultyName(), '')
        self.assertEqual(blueSheet.getFacultyEmail(), '')

    def testSetTestAccommodationsGranted(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.setTestAccommodationsRequested(['computer', 'calculator', 'extraTime'])
        self.portal.portal_workflow.doActionFor(blueSheet, 'submitToInstructor')
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('computer', 'calculator', 'extraTime')) 
        blueSheet.setTestAccommodationsGranted(['computer'])
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('computer', 'extraTime'))
        blueSheet.setTestAccommodationsGranted([''])
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('extraTime',))
        blueSheet.setTestAccommodationsGranted(['extraTime'])
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('extraTime',))
        blueSheet.setTestAccommodationsGranted(['computer', 'calculator', 'extraTime'])
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('computer', 'calculator', 'extraTime'))

    def testAllowInstructorToDropOffOrPickupTest(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        
        self.becomeLocalFaculty()
        self.assertFalse(blueSheet.areReturnAndPickupFieldsValidAndIfNotShowErrorMessage())

        blueSheet.setFacultyWillPickupTest(True)
        blueSheet.setFacultyWillDropOffTest(True)
        self.assertTrue(blueSheet.areReturnAndPickupFieldsValidAndIfNotShowErrorMessage())
        
        blueSheet.setFacultyWillPickupTest(False)
        blueSheet.setFacultyWillDropOffTest(False)
        self.assertFalse(blueSheet.areReturnAndPickupFieldsValidAndIfNotShowErrorMessage())

        blueSheet.setTestRRBuilding('Example Building')
        blueSheet.setTestRRRoom('Example Room')
        self.assertFalse(blueSheet.areReturnAndPickupFieldsValidAndIfNotShowErrorMessage())

        blueSheet.setTestPickupDate(DateTime('1/1/2001'))
        blueSheet.setTestPickupBuilding('ExampleBuilding')
        blueSheet.setTestPickupRoom('Example Room')
        self.assertTrue(blueSheet.areReturnAndPickupFieldsValidAndIfNotShowErrorMessage())

    def testTransitionsAreSkippedCorrectlyWhenInstructorWillDropOffOrPickupTest(self):
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Monday 2006/10/02').earliestTime()
        blueSheet.setTestDate(DateTime('Monday 2006/10/30'))
        portal_workflow.doActionFor(blueSheet, 'submitToInstructor')

        self.becomeLocalFaculty()
        blueSheet.setFacultyWillDropOffTest(True)
        blueSheet.setFacultyWillPickupTest(True)
        portal_workflow.doActionFor(blueSheet, 'submitToOffice')

        self.becomeStaffMember()
        blueSheet.portal_workflow.doActionFor(blueSheet, 'approveBlueSheet')
        reviewState = portal_workflow.getStatusOf('UWOshSuccessBluesheetWorkflow', blueSheet)['review_state']
        self.assertEqual(reviewState, 'waitingForInstructorToDropOffTest')

        blueSheet.portal_workflow.doActionFor(blueSheet, 'testDroppedOff')
        reviewState = portal_workflow.getStatusOf('UWOshSuccessBluesheetWorkflow', blueSheet)['review_state']
        self.assertEqual(reviewState, 'testInOffice')
        
        blueSheet.portal_workflow.doActionFor(blueSheet, 'administerTest')
        reviewState = portal_workflow.getStatusOf('UWOshSuccessBluesheetWorkflow', blueSheet)['review_state']
        self.assertEqual(reviewState, 'waitingForInstructorToPickupTest')

        blueSheet.portal_workflow.doActionFor(blueSheet, 'returnTestToInstructor')
        reviewState = portal_workflow.getStatusOf('UWOshSuccessBluesheetWorkflow', blueSheet)['review_state']
        self.assertEqual(reviewState, 'testWasReturnedToInstructor')

    def testIsTestDateLessThanThreeDaysAway(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Monday 2009/10/19').earliestTime()
        blueSheet.setTestDate('Wednesday 2009/10/21')
        self.assertTrue(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Thursday 2009/10/22')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Friday 2009/10/23')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())

        blueSheet.getCurrentDate = lambda: DateTime('Wednesday 2009/10/21').earliestTime()
        blueSheet.setTestDate('Sunday 2009/10/25')
        self.assertTrue(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Monday 2009/10/26')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Tuesday 2009/10/27')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())

        blueSheet.getCurrentDate = lambda: DateTime('Friday 2009/10/23').earliestTime()
        blueSheet.setTestDate('Tuesday 2009/10/27')
        self.assertTrue(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Wednesday 2009/10/28')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Thursday 2009/10/29')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())

        blueSheet.getCurrentDate = lambda: DateTime('Saturday 2009/10/17').earliestTime()
        blueSheet.setTestDate('Tuesday 2009/10/20')
        self.assertTrue(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Wednesday 2009/10/21')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())
        blueSheet.setTestDate('Thursday 2009/10/22')
        self.assertFalse(blueSheet.isTestDateLessThanThreeBusinessDaysAway())

    def isTestDateDuringFinals(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.getFinalSemesterDate = lambda: DateTime('Friday 2009/10/16').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/02')
        self.assertFalse(blueSheet.isTestDateDuringFinals())
        blueSheet.setTestDate('Saturday 2009/10/03')
        self.assertTrue(blueSheet.isTestDateDuringFinals())
        blueSheet.setTestDate('Sunday 2009/10/04')
        self.assertTrue(blueSheet.isTestDateDuringFinals())

    def testIsTestDateLessThanThreeWeeksAway(self):
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Friday 2009/10/02').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/23')
        self.assertFalse(blueSheet.isTestDateLessThanThreeWeeksAway())
        blueSheet.setTestDate('Thursday 2009/10/22')
        self.assertTrue(blueSheet.isTestDateLessThanThreeWeeksAway())
        blueSheet.setTestDate('Wednesday 2009/10/21')
        self.assertTrue(blueSheet.isTestDateLessThanThreeWeeksAway())

    def testInvalidTestDateShouldShowPortalMessage(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Friday 2009/10/16').earliestTime()
        blueSheet.getFinalSemesterDate = lambda: DateTime('Thursday 2009/12/31').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/16')
        self.assertFalse(blueSheet.isTestDateValidAndIfNotShowErrorMessage())
        portalMessages = blueSheet.plone_utils.showPortalMessages()
        self.assertEqual(len(portalMessages), 1)

        blueSheet.getFinalSemesterDate = lambda: DateTime('Friday 2009/10/30').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/23')
        self.assertFalse(blueSheet.isTestDateValidAndIfNotShowErrorMessage())
        portalMessages = blueSheet.plone_utils.showPortalMessages()
        self.assertEqual(len(portalMessages), 1)

    def testValidTestDateShouldNotShowPortalMessage(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Friday 2009/10/16').earliestTime()
        blueSheet.getFinalSemesterDate = lambda: DateTime('Thursday 2009/12/31').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/23')
        self.assertTrue(blueSheet.isTestDateValidAndIfNotShowErrorMessage())
        portalMessages = blueSheet.plone_utils.showPortalMessages()
        self.assertEqual(len(portalMessages), 0)

    def testAnyTestDateShouldWorkIfStaffAreSubmitting(self):
        self.becomeStaffMember()
        blueSheet = self.createTestBlueSheet()
        blueSheet.getCurrentDate = lambda: DateTime('Friday 2009/10/16').earliestTime()
        blueSheet.getFinalSemesterDate = lambda: DateTime('Thursday 2009/10/16').earliestTime()
        blueSheet.setTestDate('Friday 2009/10/16')
        self.assertTrue(blueSheet.isTestDateValidAndIfNotShowErrorMessage())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlueSheet))
    return suite
