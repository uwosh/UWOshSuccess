from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs

from Products.UWOshSuccess.config import *
from Products.UWOshSuccess.widget import *
from Products.UWOshSuccess.utils import isSuccessDebugModeEnabled
from DateTime import DateTime
import xmlrpclib
import socket
import logging

logger = logging.getLogger('BlueSheet')
webServiceBaseURL = 'http://ws.it.uwosh.edu:8081/ws/'
webService = xmlrpclib.Server(webServiceBaseURL, allow_none=1)

schema = BaseSchema.copy() + Schema((
    
    # Student fields
    StringField(
        name='studentHeader',
        widget=ReadOnlyStringWidget(
            label=' ',
            label_msgid='UWOshSuccess_label_studentHeader',
            i18n_domain='UWOshSuccess',
        ),
        default='Student Fields:',
        schemata='default',
        write_permission='UWOshSuccess: edit student fields'
    ),
    StringField(
        name='fullName',
        widget=StringWidget(
            label='Full Name',
            label_msgid='UWOshSuccess_label_fullName',
            i18n_domain='UWOshSuccess',
        ),
        default_method="getStudentNameDefault",
        required=True,
        schemata="default",
        searchable=True,
        write_permission='UWOshSuccess: edit student fields'
    ),
    StringField(
        name='email',
        widget=StringWidget(
            label='Email',
            label_msgid='UWOshSuccess_label_email',
            i18n_domain='UWOshSuccess',
        ),
        default_method="getStudentEmailDefault",
        validators=('isEmail',),
        write_permission='UWOshSuccess: edit student fields'
    ),
    DateTimeField(
        name='testDate',
        widget=CalendarWidget(
            label="Test Date and Time",
            label_msgid='UWOshSuccess_label_testDate',
            description='Select a date that is at least 3 days ahead of the current date.',
            i18n_domain='UWOshSuccess',
        ),
        required=True,
        schemata="default",
        searchable=True,
        write_permission='UWOshSuccess: edit student fields'
    ),
    StringField(
        name='courseNumberNameFaculty',
        widget=SelectionWidget(
            format='select',
            label='Course No. - Section - Course Name - Professor Name',
            label_msgid='UWOshSuccess_label_courseNumberNameFaculty',
            i18n_domain='UWOshSuccess',
        ),
        required=True,
        vocabulary="getWSCourseNumberNameFaculty",
        schemata="default",
        searchable=True,
        write_permission='UWOshSuccess: edit student fields'
    ),
    LinesField(
        name='testAccommodationsRequested',
        widget=MultiSelectionWidget(
            format='checkbox',
            label="Accommodations Requested",
            label_msgid='UWOshSuccess_label_testAccommodationsRequested',
            i18n_domain='UWOshSuccess',
        ),
        required=True,
        schemata="default",
        default='',
        vocabulary=NamedVocabulary("""UWOshSuccessAccommodations"""),
        searchable=True,
        enforceVocabulary=True,
        write_permission='UWOshSuccess: edit student fields'
    ),
    TextField(
        name='studentComments',
        widget=TextAreaWidget(
            label="Student Comments",
            label_msgid='UWOshSuccess_label_studentComments',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        searchable=True,
        write_permission='UWOshSuccess: edit student fields'
    ),

    # Faculty fields
    StringField(
        name='facultyHeader',
        widget=ReadOnlyStringWidget(
            label=' ',
            label_msgid='UWOshSuccess_label_facultyHeader',
            i18n_domain='UWOshSuccess',
        ),
        default='Faculty Fields:',
        schemata='default',
        write_permission='UWOshSuccess: edit faculty fields'
    ),
    BooleanField(
        name='facultyWillDropOffTest',
        widget=BooleanWidget(
           label='Faculty member will drop off test',
           description='A faculty member will drop off the test at the project success office themselves.',
        ),
        default=False,
        schemata='default',
        write_permission='UWOshSuccess: edit faculty fields'
    ),
    DateTimeField(
        name='testPickupDate',
        widget=CalendarWidget(
            label="Test Pickup Date and Time",
            label_msgid='UWOshSuccess_label_testPickupDate',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit faculty fields",
        searchable=True,
    ),
    StringField(
        name='testPickupBuilding',
        widget=SelectionWidget(
            label="Test Pick-up Building",
            label_msgid='UWOshSuccess_label_testBuilding',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        vocabulary=NamedVocabulary("""UWOshBuildings"""),
        searchable=True,
        enforceVocabulary=True,
        write_permission="UWOshSuccess: edit faculty fields",
    ),
    StringField(
        name='testPickupRoom',
        widget=StringWidget(
            label="Test Pick-up Room",
            label_msgid='UWOshSuccess_label_testRoom',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit faculty fields",
        searchable=True,
    ),
    LinesField(
        name='testAccommodationsGranted',
        widget=AccommodationsGrantedMultiSelectionWidget(
            format='checkbox',
            label="Accommodations Granted",
            label_msgid='UWOshSuccess_label_testAccommodationsGranted',
            description='(These are the Accommodations requested by the student)',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        vocabulary=NamedVocabulary("""UWOshSuccessAccommodations"""),
        searchable=True,
        enforceVocabulary=True,
        write_permission="UWOshSuccess: edit faculty fields",
    ),
    BooleanField(
        name='facultyWillPickupTest',
        widget=BooleanWidget(
           label='Faculty member will pickup the test',
           description='A faculty member will pick-up the test from the project success office themselves.',
        ),
        default=False,
        schemata='default',
        write_permission='UWOshSuccess: edit faculty fields'
    ),
    StringField(
        name='testRRBuilding',
        widget=SelectionWidget(
            label="Test Requested Return Building",
            label_msgid='UWOshSuccess_label_testRRBuilding',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        vocabulary=NamedVocabulary("""UWOshBuildings"""),
        searchable=True,
        enforceVocabulary=True,
        write_permission="UWOshSuccess: edit faculty fields",
    ),
    StringField(
        name='testRRRoom',
        widget=StringWidget(
            label="Test Requested Return Room",
            label_msgid='UWOshSuccess_label_testRRRoom',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit faculty fields",
        searchable=True,
    ),
    TextField(
        name='facultyComments',
        widget=TextAreaWidget(
            label="Faculty Comments",
            label_msgid='UWOshSuccess_label_facultyComments',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit faculty fields",
        searchable=True,
    ),

    # Reader Fields
    StringField(
        name='readerHeader',
        widget=ReadOnlyStringWidget(
            label=' ',
            label_msgid='UWOshSuccess_label_readerHeader',
            i18n_domain='UWOshSuccess',
        ),
        default='Reader Fields:',
        schemata='default',
        write_permission='UWOshSuccess: edit reader fields'
    ),
    StringField(
        name='testReaderAssigned',
        widget=SelectionWidget(
            format='select',
            label="Select Reader",
            label_msgid='UWOshSuccess_label_testReaderAssigned',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        vocabulary='_getTestReadersVocabulary',
        searchable=True,
        default='',
        enforceVocabulary=True,
        write_permission='UWOshSuccess: edit reader field',
    ),

    # Office fields
    StringField(
        name='officeHeader',
        widget=ReadOnlyStringWidget(
            label=' ',
            label_msgid='UWOshSuccess_label_officeHeader',
            i18n_domain='UWOshSuccess',
        ),
        default='Office Fields:',
        schemata='default',
        write_permission='UWOshSuccess: edit office fields'
    ),
    StringField(
        name='testARBuilding',
        widget=SelectionWidget(
            label="Test Actual Return Building",
            label_msgid='UWOshSuccess_label_testARBuilding',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        vocabulary=NamedVocabulary("""UWOshBuildings"""),
        searchable=True,
        enforceVocabulary=True,
        write_permission="UWOshSuccess: edit office fields",
    ),
    StringField(
        name='testARRoom',
        widget=StringWidget(
            label="Test Actual Return Room",
            label_msgid='UWOshSuccess_label_testRoom',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit office fields",
        searchable=True,
    ),
    StringField(
        name='returnPerson',
        widget=StringWidget(
            label="Return Person",
            label_msgid='UWOshSuccess_label_returnPerson',
            i18n_domain='UWOshSuccess',
        ),
        schemata="default",
        write_permission="UWOshSuccess: edit office fields",
        searchable=True,
    ),

    # Hidden fields
    StringField(
        name='facultyEmail',
        widget=StringWidget(
            label="Faculty Email",
            label_msgid='UWOshSuccess_label_facultyEmail',
            i18n_domain='UWOshSuccess',
            visible = {"edit": "invisible", "view": "invisible"}
        ),
        searchable=True,
        schemata="default",
    ),
    StringField(
        name='facultyName',
	searchable=True,
        widget=StringWidget(
            label="Faculty Name",
            label_msgid='UWOshSuccess_label_facultyName',
            i18n_domain='UWOshSuccess',
            visible = {"edit": "invisible", "view": "invisible"}
        ),
        schemata="default",
    ),

),
)

schema["title"].required = False
schema["title"].widget.visible = {"edit": "invisible", "view": "invisible"}

metadataFields = schema.getSchemataFields('metadata')
for field in metadataFields:
    field.widget.visible = {"edit": "invisible", "view": "invisible"}

class BlueSheet(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IBlueSheet)

    meta_type = 'BlueSheet'
    _at_rename_after_creation = True

    schema = schema

    def setFullName(self, value):
        self.Schema()['fullName'].set(self, value)
        self.setTitle(value + ' Blue Sheet')

    def getStudentNameDefault(self):
        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role('UWOshSuccess.Student'):
            return member.getProperty('fullname', '')
        else:
            return ''

    def getStudentEmailDefault(self):
        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role('UWOshSuccess.Student'):
            return member.getProperty('email', '')
        else:
            return ''

    def getWSCourseNumberNameFaculty(self):
        if isSuccessDebugModeEnabled(self):
            return ['COMP SCI 331 - 001C - Programming Languages - David Furcy - furcyd@uwosh.edu',
                    'MATH 172 - 001C - Calculus II - Joan Hart - hartj@uwosh.edu']

        emailid = ''

        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role('UWOshSuccess.Student'):
            emailid = member.getProperty('email', '')
        else:
            emailid = self.getEmail()
        
        if emailid == '':
            return [' ']

        try:
            return self.getEnrolledClassesFromWebService(emailid)
        except socket.error:
            try:
                return self.getEnrolledClassesFromWebService(emailid)
            except socket.error:
                logger.error('Unable to connect to: %s' % webServiceBaseURL)
                return [' ']

    def getEnrolledClassesFromWebService(self, emailid):
        enrolledClasses = []
        emplid = webService.getEmplidFromEmailAddressCX(emailid)
        strm = webService.getCurrentSemesterCX()

        if strm == "error: no semester code found matching current date":
            logger.error('No current semester')
            return [' ']

        value = webService.getEnrolledClassesCX(emplid, strm)
        retlist = xmlrpclib.loads(value)

        try:
            for row in retlist[0]:
                courseDept = row[0]
                courseNumber = row[1]
                courseSection = row[3] 
                courseName = row[2]
                facultyFirstName = row[5]
                facultyLastName = row[6]
                facultyEmail = row[7]
                rowString = '%s %s - %s - %s - %s %s - %s' % (courseDept, courseNumber, courseSection, courseName, facultyFirstName, facultyLastName, facultyEmail)
                enrolledClasses.append(rowString)
        except:
            logger.error('No enrolled classes were returned by the web service')
            enrolledClasses.append('*** Error: no enrolled classes were returned by the web service ***')
        return enrolledClasses

    def setCourseNumberNameFaculty(self, value):
        self.Schema()['courseNumberNameFaculty'].set(self, value)

        if value.count('-') == 4:
            (_, _, _, _, facEmail) = value.split('-')
            facEmail = facEmail.strip()
            (facMemberId, _) = facEmail.split('@')
            self.setFacultyEmail(facEmail)
            self.setFacultyName(facMemberId)
        else:
            self.setFacultyEmail('')
            self.setFacultyName('')

    def setTestAccommodationsGranted(self, value):
        alwaysAllowableAccommodationsVocabulary = self.portal_vocabularies.getVocabularyByName('UWOshSuccessAlwaysAllowableAccommodations')
        alwaysAllowableAccommodations = alwaysAllowableAccommodationsVocabulary.getVocabularyDict()

        requestedAccommodations = self.getTestAccommodationsRequested()
        
        for accommodation in requestedAccommodations:
            if accommodation in alwaysAllowableAccommodations and not accommodation in value:
                value.append(accommodation)

        self.Schema()['testAccommodationsGranted'].set(self, value)

    def _getTestReadersVocabulary(self):
        readersList = [(' ',' '),]

        portal_membership = getToolByName(self, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()

        if member.has_role('UWOshSuccess.Reader'):
            selectedReaderId = self.getTestReaderAssigned()
            if selectedReaderId not in [' ', '', member.id]:
                selectedReaderMember = portal_membership.getMemberById(selectedReaderId)
                selectedReaderName = selectedReaderMember.getProperty('fullname')
                readersList = [(selectedReaderId, selectedReaderName),]
            else:
                readersList.append((member.id, member.getProperty('fullname')))
        else:
            portal_groups = getToolByName(self, 'portal_groups')
            readersGroup = portal_groups.getGroupById('UWOshSuccess.Readers')
            readersGroupMembers = readersGroup.getGroupMembers()
            for member in readersGroupMembers:
                readersList.append((member.id, member.getProperty('fullname')))

        return readersList

    def areReturnAndPickupFieldsValidAndIfNotShowErrorMessage(self):
        if (self.facultyWillPickupTest == False and \
            (self.testRRBuilding == '' or self.testRRRoom == '')) \
           or \
           (self.facultyWillDropOffTest == False and \
            (self.testPickupDate == '' or self.testPickupBuilding == '' or self.testPickupRoom == '')):

            self.addPortalMessage('faculty-must-select-test-pickup-dropoff-warning', type='info')
            return False
            
        else:
            return True

    def isTestDateValidAndIfNotShowErrorMessage(self):
        member = self.portal_membership.getAuthenticatedMember()
        if not member.has_role('UWOshSuccess.Student'):
            return True

        if self.isTestDateDuringFinals14WSession() and self.isTestDateLessThanThreeWeeksAway():
            self.addPortalMessage('test-date-during-finals-week-warning', type='error')
            return False

        elif self.isTestDateLessThanThreeBusinessDaysAway():
            self.addPortalMessage('test-date-less-than-three-days-away-warning', type='error')
            return False

        else:
            return True

    def addPortalMessage(self, messageId, type='info'):
        messageText = self._lookupMessageText(messageId)
        plone_utils = getToolByName(self, 'plone_utils')
        plone_utils.addPortalMessage(messageText, type)

    def _lookupMessageText(self, messageId):
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog.searchResults({'portal_type':'Document', 'id':messageId})
        try:
            brain = brains[0]
            obj = brain.getObject()
            return obj.getText()
        except:
            return "An error has occurred but the exact error message '%s' cannot be found" % messageId

    def isTestDateDuringFinals14WSession(self):
        TWO_WEEKS = 14

        final14WSessionDate = self.getFinal14WSessionDate()

        if final14WSessionDate is None:
            return False
        else:
            return self.getTestDate() + TWO_WEEKS > final14WSessionDate

    def isTestDateLessThanThreeWeeksAway(self):
        THREE_WEEKS = 21
        return self.getCurrentDate() + THREE_WEEKS > self.getTestDate()

    def isTestDateLessThanThreeBusinessDaysAway(self):
        numberOfDaysNeeded = 3
        WED, THUR, FRI, SAT = range(3,7)

        currentDate = self.getCurrentDate()
        currentDayOfTheWeek = currentDate.dow()
        if currentDayOfTheWeek in [WED, THUR, FRI]:
            numberOfDaysNeeded += 2
        elif currentDayOfTheWeek == SAT:
            numberOfDaysNeeded += 1
        return currentDate + numberOfDaysNeeded > self.getTestDate()

    def getFinal14WSessionDate(self):
        # BUG: throws Fault: <Fault -1: 'Unexpected Zope exception: exceptions.TypeError - cannot marshal   objects'>
        #      http://www.uwosh.edu/ploneprojects/resources/issue-trackers/web-services/7
        try:
            finalDate = webService.get14WSessionUgradEndDateCX()
        except socket.error:
            try:
                 finalDate = webService.get14WSessionUgradEndDateCX()
            except socket.error:
                logger.error('Unable to connect to: %s' % webServiceBaseURL)
                return None
        if finalDate != "not a 14W session":
            return DateTime(finalDate).earliestTime()
        else:
            return None

    def getCurrentDate(self):
        return DateTime().earliestTime()


registerType(BlueSheet, PROJECTNAME)

