"""
Ensures database has had its private data removed
"""

import unittest
from datatest import DataTestCase

###--- Globals ---###

###--- Classes ---###

# Is: a bundle of tests to be executed by the standard unittest module.
class PrivateDataTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = []		# list of strings, each the name of a cache load that needs to be run if this test fails

	# list of strings, each a (non-cache load) fix that needs to be run if this test fails
	otherFixes = [ 'run pgdbutilities/sp/MGI_deletePrivateData.csh script' ]

	def setUp(self):
		# can optionally override this standard method to perform any tasks needed before executing test
		# methods in this class; just delete this if unnecessary.
		
		pass

	def testAlleleStatus(self):
		cmd = '''select 1
			from ALL_Allele a
			where a._Allele_Status_key not in (847114, 3983021)
			limit 1'''
		self.assertQueryCount(0, cmd, 'Alleles present with status other than Approved or Autoload')

	def testMixedAlleles(self):
		cmd = '''select a._Allele_key
			from ALL_Allele a
			where a.isMixed = 1
				and not exists (SELECT 1 FROM GXD_AlleleGenotype g WHERE a._Allele_key = g._Allele_key)
			limit 1'''
		self.assertQueryCount(0, cmd, 'Mixed alleles present that are not part of a genotype')
		
	def testAllelesOfReservedMarkers(self):
		cmd = '''select a._Allele_key
			from ALL_Allele a, MRK_Marker m
			where a._Marker_key = m._Marker_key
				and m._Marker_Status_key = 3
			limit 1'''
		self.assertQueryCount(0, cmd, 'Alleles of reserved markers are present')
		
	def testPrivateStrains(self):
		cmd = '''select 1
			from PRB_Strain 
			where private = 1
				and not exists (select 1 from GXD_Genotype
					where PRB_Strain._Strain_key = GXD_Genotype._Strain_key)
			limit 1'''
		self.assertQueryCount(0, cmd, 'Private strains are present that are not part of genotypes')
		
	def testReservedMarkers(self):
		cmd = '''select 1
			from MRK_Marker
			where _Marker_Status_key = 3
			limit 1'''
		self.assertQueryCount(0, cmd, 'Reserved markers are present')
		
	def testExpressionAssays(self):
		cmd = '''select 1
			from GXD_Assay
			where not exists (select 1 from GXD_Expression
				where GXD_Assay._Assay_key = GXD_Expression._Assay_key)
			limit 1'''
		self.assertQueryCount(0, cmd, 'Some expression assays not in expression cache')
		
	def testExpressionIndex(self):
		cmd = '''select 1
			from GXD_Index gi
			where not exists (select 1 from GXD_Index_Stages gis
				where gis._Index_key = gi._Index_key)
			limit 1'''
		self.assertQueryCount(0, cmd, 'Some expression index records exist without stages')
		
	def testNotes(self):
		cmd = '''select 1
			from MGI_Note n, MGI_NoteType nt 
			where n._NoteType_key = nt._NoteType_key 
				and nt.private = 1
			limit 1'''
		self.assertQueryCount(0, cmd, 'Private notes are present')
			
	def testGOAnnotations(self):
		cmd = '''select 1
			from VOC_Annot a, VOC_Term t
			where a._AnnotType_key = 1000
				and a._Term_key = t._Term_key
				and t.isObsolete = 1
			limit 1'''
		self.assertQueryCount(0, cmd, 'GO Annotations to obsolete terms are present')
		
###--- Functions ---###

def suite():
	# used to pull together a test suite from the above classes that bundle the tests.  Make sure each class
	# is added to the suite after passing through makeSuite()

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(PrivateDataTestCase))
	return suite

###--- Main Program ---###

if __name__ == '__main__':
	unittest.main()