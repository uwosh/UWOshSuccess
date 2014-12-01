from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.UWOshSuccess.config import *
from Products.UWOshSuccess.utils import isSuccessDebugModeEnabled

import xmlrpclib
import socket
import logging

logger = logging.getLogger('StudentApplication')
webServiceBaseURL = 'http://ws.it.uwosh.edu:8081/ws/'
webService = xmlrpclib.Server(webServiceBaseURL, allow_none=1)

schema = BaseSchema.copy() + Schema((

    StringField(
        name='emplid',
        widget=StringWidget(
            label='Employee Id',
            label_msgid='UWOshSuccess_label_emplid',
            i18n_domain='UWOshSuccess',
        ),
        default_method="getEmplidDefault",
        required=1,
    ),
    StringField(
        name='email',
        widget=StringWidget(
            label='Email',
            label_msgid='UWOshSuccess_label_email',
            i18n_domain='UWOshSuccess',
        ),
        default_method="getEmailDefault",
        validators =('isEmail',), 
        required=1,
    ),
    StringField(
        name='homePhone',
        widget=StringWidget(
            label='Home phone',
            label_msgid='UWOshSuccess_label_homePhone',
            i18n_domain='UWOshSuccess',
        ),
    ),
    StringField(
        name='mobilePhone',
        widget=StringWidget(
            label='Mobile phone',
            label_msgid='UWOshSuccess_label_mobilePhone',
            i18n_domain='UWOshSuccess',
        ),
    ),
    StringField(
        name='otherPhone',
        widget=StringWidget(
            label='Other phone',
            label_msgid='UWOshSuccess_label_otherPhone',
            i18n_domain='UWOshSuccess',
        ),
    ),
    StringField(
        name='fullName',
        widget=StringWidget(
            label='Full Name',
            label_msgid='UWOshSuccess_label_fullName',
            i18n_domain='UWOshSuccess',
        ),
        default_method="getFullNameDefault",
        required=1,
    ),

),
)

schema["title"].required = False
schema["title"].widget.visible = {"edit": "invisible", "view": "invisible"}

class StudentApplication(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IStudentApplication)

    meta_type = 'StudentApplication'
    _at_rename_after_creation = True

    schema = schema

    def setFullName(self, value):
        self.Schema()['fullName'].set(self, value)
        self.setTitle(value + ' Student Application')

    def getFullNameDefault(self):
        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role(['UWOshSuccess.OfficeStaff', 'Manager', 'UWOshSuccess.Faculty', 'UWOshSuccess.Director']):
            return ''
        else:
            return member.getProperty('fullname', '')

    def getEmailDefault(self):
        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role(['UWOshSuccess.OfficeStaff', 'Manager', 'UWOshSuccess.Faculty', 'UWOshSuccess.Director']):
            return ''
        else:
            return member.getProperty('email', '')

    def getEmplidDefault(self):
        if isSuccessDebugModeEnabled(self):
            return '0123456'

        pm = self.portal_membership
        member = pm.getAuthenticatedMember()
        if member.has_role(['UWOshSuccess.OfficeStaff', 'Manager', 'UWOshSuccess.Faculty', 'UWOshSuccess.Director']):
            return ''
        else:
            emailid = member.getProperty('email', '')
            return self._getEmplidFromEmailAddress(emailid)

    def _getEmplidFromEmailAddress(self, emailid):
        try:
            return webService.getEmplidFromEmailAddressCX(emailid)
        except socket.error:
            try:
                return webService.getEmplidFromEmailAddressCX(emailid)
            except socket.error:
                logger.error('Unable to connect to: %s' % webServiceBaseURL)
                return ''


registerType(StudentApplication, PROJECTNAME)


