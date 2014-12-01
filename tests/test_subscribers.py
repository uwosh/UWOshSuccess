import unittest
from Testing import ZopeTestCase as ztc

from Products.UWOshSuccess.tests.base import UWOshSuccessTestCase
from Products.UWOshSuccess.tests.mock import MockEvent
from Products.UWOshSuccess import subscribers
from Products.CMFCore.utils import getToolByName


class TestSetup(UWOshSuccessTestCase):

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testAddNewStudentToStudentsGroup(self):
        member = self.portal.portal_membership.getMemberById('test_user_1_')
        groups = sorted(member.getGroups())
        roles = sorted(member.getRoles())
        self.assertTrue('UWOshSuccess.Students' not in groups)
        self.assertTrue('UWOshSuccess.Student' not in roles)

        studentApp = self.createTestStudentApplication()
        studentApp.setEmail('test_user_1_@uwosh.edu')
        approveApplicationEvent = MockEvent(transitionId='approveApplication')

        subscribers.addNewStudentToStudentsGroup(studentApp, approveApplicationEvent)
        
        member = self.portal.portal_membership.getMemberById('test_user_1_')
        groups = sorted(member.getGroups())
        roles = sorted(member.getRoles())
        self.assertTrue('UWOshSuccess.Students' in groups)
        self.assertTrue('UWOshSuccess.Student' in roles)

    def testAddNewStudentToStudentsGroupDoesNothingOnDiffTransition(self):
        member = self.portal.portal_membership.getMemberById('test_user_1_')
        groups = sorted(member.getGroups())
        roles = sorted(member.getRoles())
        self.assertTrue('UWOshSuccess.Students' not in groups)
        self.assertTrue('UWOshSuccess.Student' not in roles)

        studentApp = self.createTestStudentApplication()
        studentApp.setEmail('test_user_1_@uwosh.edu')
        approveApplicationEvent = MockEvent(transitionId='submitToOffice')

        subscribers.addNewStudentToStudentsGroup(studentApp, approveApplicationEvent)
        
        member = self.portal.portal_membership.getMemberById('test_user_1_')
        groups = sorted(member.getGroups())
        roles = sorted(member.getRoles())
        self.assertTrue('UWOshSuccess.Students' not in groups)
        self.assertTrue('UWOshSuccess.Student' not in roles)
 
    def testCopyRequestedAccommodationsToGrantedAccommodations(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.setTestAccommodationsRequested(['calculator', 'computer'])
        submitToInstructorEvent = MockEvent(transitionId='submitToInstructor')
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ())
        subscribers.copyRequestedAccommodationsToGrantedAccommodations(blueSheet, submitToInstructorEvent)
        self.assertEqual(blueSheet.getTestAccommodationsGranted(), ('calculator', 'computer'))
        
    def testAddFacultyLocalRole(self):
        self.addFacultyToSite([('facultydan', 'Faculty Dan'), ('facultystan', 'Faculty Stan')])
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.setFacultyName('facultydan')
        submitToInstructorEvent = MockEvent(transitionId='submitToInstructor')

        self.assertEqual(blueSheet.get_local_roles(), (('test_user_1_', ('Owner',)),)) 
        subscribers.addLocalFacultyRole(blueSheet, submitToInstructorEvent)
        self.assertEqual(blueSheet.get_local_roles(), (('facultydan',('UWOshSuccess.LocalFaculty',)), ('test_user_1_', ('Owner',))))

    def testSendEmail(self):
        self.becomeStudent()
        blueSheet = self.createTestBlueSheet()
        blueSheet.setTestDate('2010/11/4')
        mailHost = self.portal.MailHost
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(len(mailHost.sentEmails), 0)
        portal_workflow.doActionFor(blueSheet, 'submitToInstructor', 'UWOshSuccessBluesheetWorkflow')
        self.assertEqual(len(mailHost.sentEmails), 1)
        sentEmail = mailHost.sentEmails[0]
        self.assertEqual(len(sentEmail['mto']), 3)
        self.assertEqual(sentEmail['mfrom'], 'successadmin@uwosh.edu')
        self.assertEqual(sentEmail['subject'], 'John Doe Blue Sheet is now Pending Instructor Review')
        self.assertTrue('The following bluesheet has been submitted to the instructor.' in sentEmail['messageText'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
