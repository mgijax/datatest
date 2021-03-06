"""
Example for building new tests
"""

import unittest
from datatest import DataTestCase

###--- Globals ---###

###--- Classes ---###

# Is: a bundle of tests to be executed by the standard unittest module.
class TemplateTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = []		# list of strings, each the name of a cache load that needs to be run if this test fails
	otherFixes = []		# list of strings, each a (non-cache load) fix that needs to be run if this test fails

	def setUp(self):
		# can optionally override this standard method to perform any tasks needed before executing test
		# methods in this class; just delete this if unnecessary.
		
		pass

	def testMethod1(self):
		# Contains a single test to be executed.  Should end with a call to an assert method:
		#	self.assertQueryCount(...)
		#	self.assertDataEquals(...)
		#	self.assertDataTrue(...)
		# Multiple test methods can be included, but each should be named beginning with "test" so they
		# can be automatically discovered.

		pass

###--- Functions ---###

def suite():
	# used to pull together a test suite from the above classes that bundle the tests.  Make sure each class
	# is added to the suite after passing through makeSuite()

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TemplateTestCase))
	return suite

###--- Main Program ---###

# tests can be executed as individual files, not just run through testPublic
if __name__ == '__main__':
	unittest.main()