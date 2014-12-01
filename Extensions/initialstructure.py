
from Products.CMFCore.utils import getToolByName

warningMessages = {
    'faculty-must-select-test-pickup-dropoff-warning' : { 
        'type' : 'Document',
        'title' : 'Faculty Must Select Test Pickup/Drop-Off - Warning',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'FOR INSTRUCTOR: You must either select that you will pickup/drop-off the test yourself; \
                  or enter the pickup/dropoff dates, rooms, and buildings.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'test-date-during-finals-week-warning' : { 
        'type' : 'Document',
        'title' : 'Test Date During Finals Week - Warning',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'FOR STUDENT: You must submit this form at least 3 weeks before the test date \
                  because the test date falls during finals week. Please contact the Project Success office.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'test-date-less-than-three-days-away-warning' : { 
        'type' : 'Document',
        'title' : 'Test Date Less Than Three Days Away - Warning',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'FOR STUDENT: You must submit this form at least 3 business days before the \
                  test date. Please contact the Project Success office.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
}

emailMessages = {
    'blue-sheet-administertest-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Administer Test - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following bluesheet has been administered.',
        'localRoles' :[('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-approvebluesheet-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Approve BlueSheet - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following bluesheet has been approved.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-beginwaitingforinstructortodropofftest-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Begin Waiting For Instructor To Drop-Off Test - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The office is waiting for the instructor to drop-off the test for the following bluesheet.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-beginwaitingforinstructortopickuptest-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Begin Waiting For Instructor to Pickup Test - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The office is waiting for the instructor to pickup the test for the following bluesheet.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-pickuptest-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Pickup Test - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The test for the following bluesheet needs to be picked up.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-preparetestforreturn-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Prepare Test For Return - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The test for the following bluesheet has been prepared for return.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-returntesttoinstructor-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Return Test to Instructor - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The test for the following bluesheet is ready to be returned to the instructor.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-submittoinstructor-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Submit to Instructor - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following bluesheet has been submitted to the instructor.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-submittooffice-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Submit To Office - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following bluesheet has been submitted to the office.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'blue-sheet-testpickedup-email-message' : { 
        'type' : 'Document',
        'title' : 'Blue Sheet - Test Picked Up - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The test for the following bluesheet has been picked up.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'student-application-approveapplication-email-message' : { 
        'type' : 'Document',
        'title' : 'Student Application - Approve Application - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following student application has been approved.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
    'student-application-submittooffice-email-message' : { 
        'type' : 'Document',
        'title' : 'Student Application - Submit To Office - Email Message',
        'excludeFromNav' : True,
        'published' : True,
        'text' : 'The following student application has been submitted to the office.',
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader', 'Editor'])]
        },
}

root = {
    'bluesheets' : { 
        'type' : 'DropboxFolder',
        'description' : 'Container for BlueSheets',
        'title' : 'Bluesheets Folder',
        'excludeFromNav' : True 
        },
    'students' : { 
        'type' : 'DropboxFolder',
        'description' : 'Container for Students',
        'title' : 'Students Folder',
        'excludeFromNav' : True 
        },
    'project-success-welcome' : { 
        'type' : 'Document',
        'published' : True,
        'title' : 'Welcome to the UW Oshkosh Project Success Site.',
        'description' : 'This is the site for student registration and Blue Sheet submission.',
        'text' : "<strong>Project Success is a remedial program for students with language-based \
                  learning disabilities attending the University of Wisconsin Oshkosh. Currently \
                  the program serves approximately 290 students who come from Wisconsin, the Midwest, \
                  and from as far away as New York, California and foreign countries to enter the program.\n\n \
                  There is no charge for Project Success services during the academic year above and beyond \
                  the student's normal resident or nonresident tuition.\n\n \
                  We hope you find our Web page easy to use and informative. If you have questions or comments \
                  about Project Success or this Web page, please contact Teri Wegner by e-mail at wegner@uwosh.edu</strong>"
        },
    'email-messages' : { 
        'type' : 'Folder', 
        'description' : 'Container for custom workflow email messages',
        'title' : 'Email Messages',
        'excludeFromNav' : True,
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader'])],
        'children' : emailMessages
        },
    'warning-messages' : { 
        'type' : 'Folder', 
        'description' : 'Container for custom warning messages',
        'title' : 'Warning Messages',
        'excludeFromNav' : True,
        'localRoles' : [('UWOshSuccess.OfficeStaff', ['Reader'])],
        'children' : warningMessages
        },
}

def publishObject(context, object):
    wft = getToolByName(context, 'portal_workflow')
    if wft.getInfoFor(object, 'review_state') != 'published':
        wft.doActionFor(object, 'publish')

def addLocalRolesToObject(object, localRoles):
    for (principal, roles) in localRoles:
        object.manage_addLocalRoles(principal, roles)

def installObject(context, id, properties):
    context.invokeFactory(properties['type'], id)
    object = context[id]
    if properties.has_key('description'):
        object.setDescription(properties['description'])
    if properties.has_key('title'):
        object.setTitle(properties['title'])
    if properties.has_key('text'):
        object.setText(properties['text'])
    if properties.has_key('published') and properties['published']:
        publishObject(context, object)
    if properties.has_key('excludeFromNav'):
        object.setExcludeFromNav(properties['excludeFromNav'])
    if properties.has_key('localRoles'):
        addLocalRolesToObject(object, properties['localRoles'])
    if properties.has_key('children'):
        installObjects(object, properties['children'])
    object.reindexObject()

def installObjects(context, structure):
    for id in structure:
        if not hasattr(context, id):
            installObject(context, id, structure[id])

def installInitialStructure(self):
    if 'Manager' not in self.REQUEST.AUTHENTICATED_USER.getRoles():
        return 'Failure. You are not a manager.'

    elif not hasattr(self, 'meta_type') or self.meta_type != 'Plone Site':
        return 'Failure. This script must be run at the Plone site root.'

    else:
        installObjects(self, root)
        return 'Success.'
