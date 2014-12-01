
from Products.CMFCore.utils import getToolByName

def getPortal(context):
    portal_url = getToolByName(context, 'portal_url')
    return portal_url.getPortalObject()

def isSuccessDebugModeEnabled(context):
    portal = getPortal(context)
    return (hasattr(portal, 'success_debug_mode') and portal.success_debug_mode)

def getSuccessDebugModeEmailAddress(context):
    portal = getPortal(context)
    if not hasattr(portal, 'success_debug_mode_email_address'):
        return ''
    else:
        return portal.success_debug_mode_email_address

def getSuccessCCEmailAddress(context):
    portal = getPortal(context)
    if not hasattr(portal, 'success_cc_email_address'):
        return 'successadmin@uwosh.edu'
    else:
        return portal.success_debug_mode_email_address
