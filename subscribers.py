from Products.CMFCore.utils import getToolByName
from Products.UWOshSuccess.utils import isSuccessDebugModeEnabled, getSuccessDebugModeEmailAddress, getSuccessCCEmailAddress
import logging

logger = logging.getLogger('subscribers')

def _convertToId(string):
    string = string.lower()
    string = string.replace(' ', '-')
    return string

def _lookupEmailBody(context, type, transition):
    portal_catalog = getToolByName(context, 'portal_catalog')
    documentId = '%s-%s-email-message' % (_convertToId(type), _convertToId(transition))
    brains = portal_catalog.searchResults({'portal_type':'Document', 'id':documentId})
    try:
        brain = brains[0]
        obj = brain.getObject()
        return obj.getText()
    except:
        logger.error('Unable to locate email message template with ID: %s' % documentId)
        return "The following item has been transitioned: "

blueSheetEmailRecipients = { 
    'submitToInstructor' : ['faculty', 'student', 'office'],
    'submitToOffice' : ['faculty', 'student', 'office'],
    'approveBlueSheet' : ['faculty', 'student', 'office'],
    'beginWaitingForInstructorToDropOffTest' : ['faculty', 'office'],
    'pickUpTest' : ['faculty', 'office'],
    'testPickedUp' : ['faculty', 'office'],
    'administerTest' : ['faculty', 'office'],
    'beginWaitingForInstructorToPickupTest' : ['faculty', 'office'],
    'prepareTestForReturn' : ['faculty', 'office'],
    'returnTestToInstructor' : ['faculty', 'office'],
    }

studentApplicationEmailRecipients = { 
    'submitToOffice' : ['student', 'office'],
    'approveApplication' : ['student', 'office'],
    }

blueSheetTransitions = blueSheetEmailRecipients.keys()
studentApplicationTransitions = studentApplicationEmailRecipients.keys()

def sendNotificationEmails(obj, event):
    if not event.transition:
        return

    objType = obj.Type()
    transitionId = event.transition.id

    if objType == 'Blue Sheet' and (transitionId in blueSheetTransitions):
        recipients = blueSheetEmailRecipients[transitionId]
    elif objType == 'Student Application' and (transitionId in studentApplicationTransitions):
        recipients = studentApplicationEmailRecipients[transitionId]
    else:
        return

    newStateTitle = event.new_state.title
    objTitle = obj.Title()
    officeEmail = getSuccessCCEmailAddress(obj)
    
    mTo = []
    if 'student' in recipients:
        mTo.append(obj.getEmail())
    if 'faculty' in recipients:
        mTo.append(obj.getFacultyEmail())
    if 'office' in recipients:
        mTo.append(officeEmail)

    mFrom = officeEmail
    mSubj = '%s is now %s' % (objTitle, newStateTitle)
    mBody = _lookupEmailBody(obj, objType, transitionId)
    mBody = '%s\n\n%s' % (mBody, obj.absolute_url())
        
    if isSuccessDebugModeEnabled(obj):
        mTo = []

        emailAddress = getSuccessDebugModeEmailAddress(obj)
        if emailAddress != '':
            for recipient in recipients:
                mTo.append(emailAddress.replace('@', '+%s@' % recipient))
            
    obj.MailHost.send(mBody, mTo, mFrom, mSubj)


def addNewStudentToStudentsGroup(obj, event):
    if not event.transition or not event.transition.id == 'approveApplication':
        return

    email = obj.getEmail()
    (memberId, _) = email.split('@')

    portal_groups = getToolByName(obj, 'portal_groups')
    portal_groups.addPrincipalToGroup(memberId, 'UWOshSuccess.Students')
    
        
def copyRequestedAccommodationsToGrantedAccommodations(obj, event):
    if not event.transition or not event.transition.id == 'submitToInstructor':
        return

    requestedAccommodations = obj.getTestAccommodationsRequested()
    obj.setTestAccommodationsGranted(requestedAccommodations)


def addLocalFacultyRole(obj, event):
    if not event.transition or not event.transition.id == 'submitToInstructor':
        return

    facultyId = obj.getFacultyName()
    obj.manage_addLocalRoles(facultyId, ['UWOshSuccess.LocalFaculty',])

