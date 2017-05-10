"""
Ensures that genotypes with MP annotations also have MP headers defined in VOC_AnnotHeader
"""

import unittest
from datatest import DataTestCase

###--- Globals ---###

###--- Classes ---###

# Is: a bundle of tests to be executed by the standard unittest module.
class AnnotHeaderTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = []		# list of strings, each the name of a cache load that needs to be run if this test fails

	# list of strings, each a (non-cache load) fix that needs to be run if this test fails
	otherFixes = [ 'fix annotations missing from VOC_AnnotHeader']

	def testGenotypesWithNoHeaders(self):
		cmd = '''select 1
			from voc_annot va
			where va._AnnotType_key = 1002
				and not exists (select 1 from voc_annotheader vah
					where vah._AnnotType_key = 1002
					and va._Object_key = vah._Object_key)
			limit 1'''
		
		self.assertQueryCount(0, cmd, 'Some genotypes with MP annotations have no headers in VOC_AnnotHeader')

###--- Functions ---###

def suite():
	# used to pull together a test suite from the above classes that bundle the tests.  Make sure each class
	# is added to the suite after passing through makeSuite()

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(AnnotHeaderTestCase))
	return suite

###--- Main Program ---###

# tests can be executed as individual files, not just run through testPublic
if __name__ == '__main__':
	unittest.main()