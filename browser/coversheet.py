from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from DateTime import DateTime
from Acquisition import aq_inner


class ICoverSheet(Interface):
    pass


class CoverSheet(BrowserView):
    implements(ICoverSheet)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_membership = getToolByName(self.context, 'portal_membership')
        self._initTestInformation()

    def _initTestInformation(self):
        courseNumberNameFaculty = self.context.getCourseNumberNameFaculty()
        if courseNumberNameFaculty.count(' - ') == 4:
            (self.courseNumber, self.courseSection, self.courseName, self.professorName, _) = courseNumberNameFaculty.split(' - ')
        else:
            (self.courseNumber, self.courseSection, self.courseName, self.professorName) = ('', '', '', '')

        testDate = self.context.getTestDate()
        if testDate is None:
            self.testDate = ''
        else:
            self.testDate = testDate.strftime('%m/%d/%Y')

    def students(self):
        students = []
        testTime = self.context.getTestDate().strftime('%I:%M %p')

        searchQuery = {
            'portal_type':'BlueSheet',
            'testDate':self.context.getTestDate(),
            'courseNumberNameFaculty':self.context.getCourseNumberNameFaculty(),
            'review_state':['blueSheetApproved', 'testNeedsToBePickedUp', 'waitingForInstructorToDropOffTest', 'testInOffice']
            }
        
        brains = self.portal_catalog.searchResults(searchQuery)

        for brain in brains:
            firstName, lastName = self._splitNameIntoFirstAndLast(brain.fullName)
            readerName = self._getReaderName(brain.testReaderAssigned)
            students.append({'lastName':lastName, 'firstName':firstName, 'testTime':testTime, 'readerName':readerName})

        return students

    def _splitNameIntoFirstAndLast(self, name):
        if ' ' in name:
            return name.split(' ', 1)
        else:
            return (name, '')

    def _getReaderName(self, readerId):
        member = self.portal_membership.getMemberById(readerId)
        if member is not None:
            readerName = member.getProperty('fullname', readerId)
        else:
            readerName = readerId
        return readerName
