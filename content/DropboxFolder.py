from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.UWOshSuccess.config import PROJECTNAME
import interfaces

DropboxFolderSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((

))


DropboxFolderSchema['title'].storage = atapi.AnnotationStorage()
DropboxFolderSchema['description'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(DropboxFolderSchema, folderish=True, moveDiscussion=False)


class DropboxFolder(folder.ATBTreeFolder):
    implements(interfaces.IDropboxFolder,)

    portal_type = 'DropboxFolder'
    schema = DropboxFolderSchema

    title = atapi.ATFieldProperty('title') 
    description = atapi.ATFieldProperty('description')
    

atapi.registerType(DropboxFolder, PROJECTNAME)
