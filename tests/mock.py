
class Mock:
    pass

class MockEvent:
    """Simulates an event object like what would be passed to a subscriber from an IAfterTransitionEvent"""

    def __init__(self, transitionId='mockTransition'):
        self.transition = self.MockTransition(id=transitionId)

    class MockTransition:
        def __init__(self, id='mockTransition'):
            self.id = id


class MockMailHost(object):
    """A mock mail host to avoid actually sending emails when testing."""

    def __init__(self):
        self.sentEmails = []

    def getId(self):
        return 'MailHost'

    def send(self, messageText, mto=None, mfrom=None, subject=None, encode=None):
        sentEmail = { 'messageText':messageText, 'mto':mto, 'mfrom':mfrom, 'subject':subject, 'encode':encode }
        self.sentEmails.append(sentEmail)

    @property
    def numberOfSentEmails(self):
        return len(self.sentEmails)

class MockWebService:
    """Simulates some of the webservice stuff from Projects/WebServices/Campus_Directory_web_service"""

    def getEmplidFromEmailAddress(self, emailid):
        return '0123456'

    def getCurrentSemester(self):
        return '0635'

    def getEnrolledClasses(self, emplid, strm):
        return self.enrolledClasses

    def getCurrentSemesterUgradEndDate(self):
        return '2009-06-15'

    """ Once this big ugly hunk of text is parsed by BlueSheet.getEnrolledClassesFromWebService() you should have this:
    ['COMP SCI 331 - 001C - Programming Languages - Daniel Boone - booned@uwosh.edu',
     'COMP SCI 342 - 001C - Software Engineering II - Kathy Jones - jonesk@uwosh.edu',
     'COMP SCI 480 - 002C - Topics in Comp Sci - Robert Robertson - robertr@uwosh.edu',
     'MATH 172 - 001C - Calculus II - Jane Heart - heartj@uwosh.edu',
     'COMP SCI 446 - 002I - Com Sci Independent Study - George Sleeps - sleeps@uwosh.edu']
    """
    enrolledClasses = '<params>\n<param>\n<value><array><data>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>SUBJECT</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>CATALOG_NBR</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>DESCR</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>CLASS_SECTION</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>CRSE_ID</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>FIRST_NAME</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>LAST_NAME</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>EMAIL_ADDR</string></value>\n</member>\n</struct></value>\n<value><struct>\n<member>\n<name>width</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>null</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>type</name>\n<value><string>s</string></value>\n</member>\n<member>\n<name>name</name>\n<value><string>EMPLID</string></value>\n</member>\n</struct></value>\n</data></array></value>\n</param>\n<param>\n<value><array><data>\n<value><array><data>\n<value><string>COMP SCI</string></value>\n<value><string>331</string></value>\n<value><string>Programming Languages</string></value>\n<value><string>001C</string></value>\n<value><string>012345</string></value>\n<value><string>Daniel</string></value>\n<value><string>Boone</string></value>\n<value><string>booned@uwosh.edu</string></value>\n<value><string>3333333</string></value>\n</data></array></value>\n<value><array><data>\n<value><string>COMP SCI</string></value>\n<value><string>342</string></value>\n<value><string>Software Engineering II</string></value>\n<value><string>001C</string></value>\n<value><string>007777</string></value>\n<value><string>Kathy</string></value>\n<value><string>Jones</string></value>\n<value><string>jonesk@uwosh.edu</string></value>\n<value><string>0333333</string></value>\n</data></array></value>\n<value><array><data>\n<value><string>COMP SCI</string></value>\n<value><string>480</string></value>\n<value><string>Topics in Comp Sci</string></value>\n<value><string>002C</string></value>\n<value><string>002222</string></value>\n<value><string>Robert</string></value>\n<value><string>Robertson</string></value>\n<value><string>robertr@uwosh.edu</string></value>\n<value><string>0355454</string></value>\n</data></array></value>\n<value><array><data>\n<value><string>MATH</string></value>\n<value><string>172</string></value>\n<value><string>Calculus II</string></value>\n<value><string>001C</string></value>\n<value><string>003888</string></value>\n<value><string>Jane</string></value>\n<value><string>Heart</string></value>\n<value><string>heartj@uwosh.edu</string></value>\n<value><string>1111111</string></value>\n</data></array></value>\n<value><array><data>\n<value><string>COMP SCI</string></value>\n<value><string>446</string></value>\n<value><string>Com Sci Independent Study</string></value>\n<value><string>002I</string></value>\n<value><string>000000</string></value>\n<value><string>George</string></value>\n<value><string>Sleeps</string></value>\n<value><string>sleeps@uwosh.edu</string></value>\n<value><string>8888888</string></value>\n</data></array></value>\n</data></array></value>\n</param>\n</params>\n'
