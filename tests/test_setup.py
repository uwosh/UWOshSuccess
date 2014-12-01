import unittest
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName

from Products.UWOshSuccess.tests.base import UWOshSuccessTestCase


class TestSetup(UWOshSuccessTestCase):

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testRolesInstalledCorrectly(self):
        roles = ['UWOshSuccess.Student', 'UWOshSuccess.Faculty', 'UWOshSuccess.Director',
                 'UWOshSuccess.Reader', 'UWOshSuccess.OfficeStaff', 'UWOshSuccess.LocalFaculty']

        portal_role_manager = self.portal.acl_users.portal_role_manager
        installedRoles = portal_role_manager.listRoleIds()

        for role in roles:
            self.assertTrue(role in installedRoles)

    def testGroupsInstalledCorrectly(self):
        groups = [('UWOshSuccess.Students', 'UWOshSuccess.Student'), ('UWOshSuccess.Faculty', 'UWOshSuccess.Faculty'),
                  ('UWOshSuccess.OfficeStaff', 'UWOshSuccess.OfficeStaff'), ('UWOshSuccess.Directors', 'UWOshSuccess.Director'),
                  ('UWOshSuccess.Readers', 'UWOshSuccess.Reader'),]

        portal_groups = self.portal.portal_groups

        for (groupId, groupRole) in groups:
            group = portal_groups.getGroupById(groupId)
            self.assertTrue(group is not None)

            roles = sorted(group.getRoles())
            self.assertEqual(roles, ['Authenticated', groupRole])

    def testATVocabulariesInstalledCorrectly(self):
        portal_vocabularies = self.portal.portal_vocabularies
        vocabIds = portal_vocabularies.objectIds()
        vocabIds.sort()
        self.assertEqual(vocabIds, ['UWOshBuildings', 'UWOshSuccessAccommodations', 
                                    'UWOshSuccessAlwaysAllowableAccommodations',
                                    'UWOshSuccessTestLocations'])

        self.assertTrue(len(portal_vocabularies['UWOshBuildings'].objectIds()) >= 1)
        self.assertTrue(len(portal_vocabularies['UWOshSuccessAccommodations'].objectIds()) >= 1)
        self.assertTrue(len(portal_vocabularies['UWOshSuccessAlwaysAllowableAccommodations'].objectIds()) >= 1)
        self.assertTrue(len(portal_vocabularies['UWOshSuccessTestLocations'].objectIds()) >= 1)
 
    def testCustomContentIsInstalled(self):
        portal_workflow = getToolByName(self.portal, 'portal_workflow')

        self.assertTrue(hasattr(self.portal, 'bluesheets'))
        self.assertTrue(hasattr(self.portal, 'students'))
        self.assertTrue(hasattr(self.portal, 'project-success-welcome'))

        self.assertEqual(self.portal['bluesheets'].Type(), 'Dropbox Folder')
        self.assertEqual(self.portal['students'].Type(), 'Dropbox Folder')
        self.assertEqual(self.portal['project-success-welcome'].Type(), 'Page')

        welcomePageReviewState = self.portal.portal_workflow.getInfoFor(self.portal['project-success-welcome'], 'review_state')
        self.assertEqual(welcomePageReviewState, 'published')

    def testCustomMessagesAreInstalled(self):
        blueSheetTransitions = ['submitToInstructor', 'submitToOffice', 'approveBlueSheet',
                                'beginWaitingForInstructorToDropOffTest', 'pickUpTest',
                                'testPickedUp', 'administerTest', 'beginWaitingForInstructorToPickupTest',
                                'prepareTestForReturn', 'returnTestToInstructor']

        studentApplicationTransitions = ['submitToOffice', 'approveApplication']

        self.assertTrue(hasattr(self.portal, 'warning-messages'))
        self.assertTrue(hasattr(self.portal, 'email-messages'))
        
        emailMessagesFolder = self.portal['email-messages']

        for transition in blueSheetTransitions:
            messageId = 'blue-sheet-%s-email-message' % transition.lower()
            self.assertTrue(hasattr(emailMessagesFolder, messageId))
            self.assertTrue(len(emailMessagesFolder[messageId].getText()) > 0)

        for transition in studentApplicationTransitions:
            messageId = 'student-application-%s-email-message' % transition.lower()
            self.assertTrue(hasattr(emailMessagesFolder, messageId))
            self.assertTrue(len(emailMessagesFolder[messageId].getText()) > 0)

    def testWorkflowsAreInstalled(self):
        portal_workflow = self.portal.portal_workflow
        workflowIds = portal_workflow.objectIds()
        self.assertTrue('UWOshSuccessBluesheetWorkflow' in workflowIds)
        self.assertTrue('UWOshSuccessDropboxFolderWorkflow' in workflowIds)
        self.assertTrue('UWOshSuccessStudentApplicationWorkflow' in workflowIds)

    def testBluesheetWorkflowStatesInstalled(self):
       states = ['archived', 'blueSheetApproved', 'pendingInstructorReview',
                 'pendingOfficeReview', 'private', 'testAdministered',
                 'testInOffice', 'testNeedsToBePickedUp',
                 'testNeedsToBeReturned', 'testWasReturnedToInstructor',
                 'waitingForInstructorToDropOffTest', 'waitingForInstructorToPickupTest'
                 ]
       workflow = self.portal.portal_workflow['UWOshSuccessBluesheetWorkflow']
       installedStates = sorted(workflow.states.objectIds())
       self.assertEqual(installedStates, states)

    def testDropboxFolderWorkflowStatesInstalled(self):
        states = ['closed', 'open']
        workflow = self.portal.portal_workflow['UWOshSuccessDropboxFolderWorkflow']
        installedStates = sorted(workflow.states.objectIds())
        self.assertEqual(installedStates, states)

    def testStudentApplicationWorkflowStatesInstalled(self):
        states = ['accepted', 'private', 'underReview']
        
        workflow = self.portal.portal_workflow['UWOshSuccessStudentApplicationWorkflow']
        installedStates = sorted(workflow.states.objectIds())
        self.assertEqual(installedStates, states)
  
    def testTypesAreInstalled(self):
        portal_types = self.portal.portal_types
        installedTypes = portal_types.objectIds()
        self.assertTrue('BlueSheet' in installedTypes)
        self.assertTrue('DropboxFolder' in installedTypes)
        self.assertTrue('StudentApplication' in installedTypes)

    def testThatInlineEditingIsDisabled(self):
        portal_properties = getToolByName(self.portal, 'portal_properties')
        inlineEditingEnabled = portal_properties.site_properties.getProperty('enable_inline_editing')
        self.assertFalse(inlineEditingEnabled)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
