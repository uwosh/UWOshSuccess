import unittest
from Testing import ZopeTestCase as ztc

from Products.UWOshSuccess.tests.base import UWOshSuccessTestCase

from DateTime import DateTime


class TestStudentApplication(UWOshSuccessTestCase):
    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def testSetFullName(self):
        studentApp = self.createTestStudentApplication()
        studentApp.setFullName('John Doe')
        self.assertEqual(studentApp.getFullName(), 'John Doe')
        self.assertEqual(studentApp.Title(), 'John Doe Student Application')

    def testGetFullNameDefaultAsStaffMember(self):
        self.becomeStaffMember()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getFullNameDefault(), '')

    def testGetFullNameDefaultAsStudent(self):
        self.becomeStudent()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getFullNameDefault(), 'John Doe')

    def testGetEmailDefaultAsStudent(self):
        self.becomeStudent()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getEmailDefault(), 'test_user_1_@uwosh.edu')

    def testGetEmailDefaultAsStaffMember(self):
        self.becomeStaffMember()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getEmailDefault(), '')

    def testGetEmplidDefaultAsStudent(self):
        self.becomeStudent()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getEmplidDefault(), '0123456')

    def testGetEmplidDefaultAsStaffMember(self):
        self.becomeStaffMember()
        studentApp = self.createTestStudentApplication()
        self.assertEquals(studentApp.getEmplidDefault(), '')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStudentApplication))
    return suite
