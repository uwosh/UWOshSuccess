import logging
logger = logging.getLogger('UWOshSuccess: setuphandlers')

import os
import transaction

from config import product_globals
from Globals import package_home
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

from plone.app.kss import content_replacer

from Products.UWOshSuccess.config import PROJECTNAME
from Products.UWOshSuccess.config import DEPENDENCIES


def isNotUWOshSuccessProfile(context):
    return context.readDataFile("UWOshSuccess_marker.txt") is None

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    if isNotUWOshSuccessProfile(context):
        return 
    site = context.getSite()
    # Create vocabularies in vocabulary lib
    atvm = getToolByName(site, ATVOCABULARYTOOL)
    vocabmap = { 'UWOshSuccessTestLocations' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
                 'UWOshSuccessAccommodations' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
                 'UWOshSuccessAlwaysAllowableAccommodations' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
                 'UWOshBuildings' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
                 }

    for vocabname in vocabmap.keys():
        if not vocabname in atvm.contentIds():
            atvm.invokeFactory(vocabmap[vocabname][0], vocabname)

        if len(atvm[vocabname].contentIds()) < 1:
            if vocabmap[vocabname][0] == 'SimpleVocabulary':
                csvpath = os.path.join(package_home(product_globals), 'data', '%s.csv' % vocabname)

                if not (os.path.exists(csvpath) and os.path.isfile(csvpath)):
                    logger.warn('No csv import file provided at %s.' % csvpath)
                    continue
                try:
                    f = open(csvpath, 'r')
                    data = f.read()
                    f.close()
                except:
                    logger.warn("Problems while reading csv import file provided at %s." % csvpath)
                    continue
                atvm[vocabname].importCSV(data)

def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotUWOshSuccessProfile(context):
        return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def installCustomGroups(context):
    if isNotUWOshSuccessProfile(context):
        return  
    groupsTool = getToolByName(context.getSite(), 'portal_groups')
    groupsTool.addGroup('UWOshSuccess.Students', roles=['UWOshSuccess.Student',])
    groupsTool.addGroup('UWOshSuccess.Faculty', roles=['UWOshSuccess.Faculty',])
    groupsTool.addGroup('UWOshSuccess.OfficeStaff', roles=['UWOshSuccess.OfficeStaff',])
    groupsTool.addGroup('UWOshSuccess.Directors', roles=['UWOshSuccess.Director',])
    groupsTool.addGroup('UWOshSuccess.Readers', roles=['UWOshSuccess.Reader',])

def installExternalMethods(context):
    site = context.getSite()

    if not hasattr(site, 'UWOshSuccess_installInitialStructure'):
        manage_addExternalMethod(site,
                                 'UWOshSuccess_installInitialStructure',
                                 'UWOshSuccess_installInitialStructure',
                                 'Products.UWOshSuccess.initialstructure',
                                 'installInitialStructure'
                                 )
    
def postInstall(context):
    """Called as at the end of the setup process. """
    if isNotUWOshSuccessProfile(context):
        return
    installExternalMethods(context)
