# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "UWOshSuccess"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = { 
    'BlueSheet': 'UWOshSuccess: Add BlueSheet',
    'StudentApplication': 'UWOshSuccess: Add StudentApplication',   
    'DropboxFolder': 'UWOshSuccess: Add DropboxFolder',   
}

setDefaultRoles('UWOshSuccess: Add BlueSheet', ('Manager','Owner'))
setDefaultRoles('UWOshSuccess: Add StudentApplication', ('Manager','Owner'))
setDefaultRoles('UWOshSuccess: Add DropboxFolder',  ('Manager','Owner'))
setDefaultRoles('UWOshSuccess: edit student fields', ('Manager', 'Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []
