from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five.testbrowser import Browser

from AccessControl import Unauthorized
from mechanize._mechanize import LinkNotFoundError

import Products.ATVocabularyManager
import Products.UWOshSuccess
from Products.UWOshSuccess.content import BlueSheet
from Products.UWOshSuccess.content import StudentApplication
from Products.UWOshSuccess.Extensions.initialstructure import installInitialStructure
from Products.UWOshSuccess.tests.mock import Mock, MockMailHost, MockWebService
from smtplib import SMTPRecipientsRefused
from DateTime import DateTime

@onsetup
def setup_uwoshsuccess():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.ATVocabularyManager)
    zcml.load_config('configure.zcml', Products.UWOshSuccess)
    fiveconfigure.debug_mode = False
    ztc.installProduct('ATVocabularyManager')
    ztc.installProduct('UWOshSuccess')
    
setup_uwoshsuccess()
ptc.setupPloneSite(products=['ATVocabularyManager', 'UWOshSuccess'])


class UWOshSuccessTestCase(ptc.PloneTestCase):
    def _setup(self):
        ptc.PloneTestCase._setup(self)
        self.setupTestUser()
        self.portal.MailHost = MockMailHost()
        BlueSheet.webService = MockWebService()
        StudentApplication.webService = MockWebService()
        
        self.setRoles(['Member', 'Authenticated', 'Manager'])
        mockPortalWithRequest = self.portal
        mockPortalWithRequest.REQUEST.AUTHENTICATED_USER = Mock()
        mockPortalWithRequest.REQUEST.AUTHENTICATED_USER.getRoles = lambda: ['Manager']
        installInitialStructure(mockPortalWithRequest)
        self.setRoles(['Member', 'Authenticated'])

    def addReadersToSite(self, readers):
        self._addMembersToSite(readers, ['UWOshSuccess.Readers',])
    
    def addFacultyToSite(self, faculty):
        self._addMembersToSite(faculty, ['UWOshSuccess.Faculty',])

    def addOfficeStaffToSite(self, staff):
        self._addMembersToSite(staff, ['UWOshSuccess.OfficeStaff',])

    def _addMembersToSite(self, members, initialGroups=[]):
        for (username, fullname) in members:
            self._addMemberToSite(username, fullname, initialGroups)

    def _addMemberToSite(self, username, fullname, initialGroups=[]):
        portal_groups = getToolByName(self.portal, 'portal_groups')
        portal_registration = getToolByName(self.portal, 'portal_registration')
        properties = { 'username':username, 'fullname':fullname, 'email':(username + '@uwosh.edu') }
        password = 'secret'
        portal_registration.addMember(username, password, properties=properties)
        for group in initialGroups:
            portal_groups.addPrincipalToGroup(username, group)

    def setupTestUser(self):
        portal_membership = getToolByName(self.portal, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        member.setProperties(email='test_user_1_@uwosh.edu', fullname='John Doe')

    def createTestBlueSheet(self):
        self.folder.invokeFactory('BlueSheet', 'test-bluesheet')
        return self.folder['test-bluesheet']

    def createTestStudentApplication(self):
        self.folder.invokeFactory('StudentApplication', 'test-student-application')
        return self.folder['test-student-application']

    def becomeStudent(self):
        self.setRoles(['Authenticated', 'Member', 'UWOshSuccess.Student'])

    def becomeStaffMember(self):
        self.setRoles(['Authenticated', 'Member', 'UWOshSuccess.OfficeStaff'])

    def becomeReader(self):
        self.setRoles(['Authenticated', 'Member', 'UWOshSuccess.Reader'])

    def becomeLocalFaculty(self):
        self.setRoles(['Authenticated', 'Member', 'UWOshSuccess.Faculty', 'UWOshSuccess.LocalFaculty'])


class UWOshSuccessFunctionalTestCase(UWOshSuccessTestCase, ptc.FunctionalTestCase):

    def __init__(self, methodName='runTest'):
        UWOshSuccessTestCase.__init__(self, methodName)
        ptc.FunctionalTestCase.__init__(self, methodName)
        self.browser = Browser()
        self.browser.addHeader('Accept-Language', 'en-US')

    def browserLogout(self):
        self.browser.open(self.portal.absolute_url() + '/logout')
        self.assertTrue('You are now logged out' in self.browser.contents)

    def browserLogin(self, username, password='secret'):
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = username
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()
        self.assertTrue('You are now logged in' in self.browser.contents)
