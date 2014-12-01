from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from DateTime import DateTime
from Acquisition import aq_inner
from Products.UWOshSuccess.content.BlueSheet import BlueSheet


class IReport(Interface):
    pass


class Report(BrowserView):
    implements(IReport)

    resultTemplate = ZopeTwoPageTemplateFile('report.pt')

    statesFromOfficeApprovalToAdministerTest = ['blueSheetApproved', 'testNeedsToBePickedUp', 'testInOffice', 'waitingForInstructorToDropOffTest']
    dateFormat = '%m/%d/%Y'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_membership = getToolByName(self.context, 'portal_membership')
        self.portal_workflow = getToolByName(self.context, 'portal_workflow')

    def testsToday(self):
        today = DateTime()
        self.reportTitle = 'Tests Today: %s' % today.strftime(self.dateFormat)
        brains = self.portal_catalog.searchResults(sort_on='testDate', portal_type='BlueSheet',
                                                   review_state=self.statesFromOfficeApprovalToAdministerTest)
        filteredBrains = filter((lambda b: b['testDate'] >= today.earliestTime() and b['testDate'] <= today.latestTime()), brains)
        self.results = self._convertBrainsToResultsDict(filteredBrains)
        return self.resultTemplate()

    def testsThisWeek(self):
        today = DateTime()
        dow = today.dow()
        firstDayOfThisWeek = today - dow
        lastDayOfThisWeek = today + (6 - dow)
        self.reportTitle = 'Tests This Week: %s - %s' % (firstDayOfThisWeek.strftime(self.dateFormat), lastDayOfThisWeek.strftime(self.dateFormat))
        brains = self.portal_catalog.searchResults(sort_on='testDate', portal_type='BlueSheet',
                                                   review_state=self.statesFromOfficeApprovalToAdministerTest)
        filteredBrains = filter((lambda b: b['testDate'] >= firstDayOfThisWeek.earliestTime() and b['testDate'] <= lastDayOfThisWeek.latestTime()), brains)
        self.results = self._convertBrainsToResultsDict(filteredBrains)
        return self.resultTemplate()

    def testsNextWeek(self):
        today = DateTime()
        dow = today.dow()
        firstDayOfNextWeek = today - dow + 7
        lastDayOfNextWeek = today + (6 - dow) + 7
        self.reportTitle = 'Tests Next Week: %s - %s' % (firstDayOfNextWeek.strftime(self.dateFormat), lastDayOfNextWeek.strftime(self.dateFormat))
        brains = self.portal_catalog.searchResults(sort_on='testDate', portal_type='BlueSheet',
                                                       review_state=self.statesFromOfficeApprovalToAdministerTest)
        filteredBrains = filter((lambda b: b['testDate'] >= firstDayOfNextWeek.earliestTime() and b['testDate'] <= lastDayOfNextWeek.latestTime()), brains)
        self.results = self._convertBrainsToResultsDict(filteredBrains)
        return self.resultTemplate()

    def blueSheetsPendingFacultyApproval(self):
        self.reportTitle = 'BlueSheets Pending My Approval'
        username = self.getAuthenticatedUserUserName()
        brains = self.portal_catalog.searchResults(sort_on='modified', sort_order='reverse', portal_type='BlueSheet',
                                                   review_state=['pendingInstructorReview'], facultyName=username)
        self.results = self._convertBrainsToResultsDict(brains)
        return self.resultTemplate()

    def blueSheetsAssignedToReader(self):
        self.reportTitle = 'BlueSheets Assigned To Me'
        username = self.getAuthenticatedUserUserName()
        brains = self.portal_catalog.searchResults(sort_on='modified', sort_order='reverse', portal_type='BlueSheet',
                                                   review_state=self.statesFromOfficeApprovalToAdministerTest, testReaderAssigned=username)
        self.results = self._convertBrainsToResultsDict(brains)
        return self.resultTemplate()
    
    def blueSheetsWithoutAnAssignedReader(self):
        self.reportTitle = 'BlueSheets Without An Assigned Reader'
        brains = self.portal_catalog.searchResults(sort_on='modified', sort_order='reverse', portal_type='BlueSheet',
                                                   review_state=self.statesFromOfficeApprovalToAdministerTest, testReaderAssigned=['', ' '])
        filteredBrains = filter((lambda b: 'humanReader' in b.testAccommodationsRequested), brains)
        self.results = self._convertBrainsToResultsDict(filteredBrains)
        return self.resultTemplate()

    def allBlueSheets(self):
        self.reportTitle = 'All BlueSheets'
        brains = self.portal_catalog.searchResults(sort_on='modified', portal_type='BlueSheet', sort_order='reverse')
        self.results = self._convertBrainsToResultsDict(brains)
        return self.resultTemplate()
        
    def _convertBrainsToResultsDict(self, brains):
        results = []

        for brain in brains:
            testAccommodationsDict = BlueSheet.schema['testAccommodationsRequested'].vocabulary.getVocabularyDict(self)

            accommodationTitles = []
            for accommodationId in brain.testAccommodationsRequested:
                if testAccommodationsDict.has_key(accommodationId):
                    accommodationTitle = testAccommodationsDict[accommodationId]
                    accommodationTitles.append(accommodationTitle)

            testAccommodationsRequested = ', '.join(accommodationTitles)
            reviewStateTitle = self.portal_workflow.getTitleForStateOnType(brain['review_state'], 'BlueSheet')
            

            result = { 'url' : brain.getObject().absolute_url(),
                       'title' : brain.Title,
                       'courseNumberNameFaculty' : brain.courseNumberNameFaculty, 
                       'testAccommodationsRequested' : testAccommodationsRequested,
                       'reviewState' : reviewStateTitle
                     }
            results.append(result)

        return results

    def getAuthenticatedUserUserName(self):
        member = self.portal_membership.getAuthenticatedMember()
        username = member.getUserName()
        return username
