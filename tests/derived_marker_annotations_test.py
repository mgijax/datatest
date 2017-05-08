"""
Test the derived marker annotations (e.g. MP and DO)
	which come from the rollupload
"""

import unittest
from datatest import DataTestCase, runQuery

### Constants ###
# Mammalian Phenotype/Genotype
MP_GENO_TYPE_KEY = 1002
# Mammalian Phenotype/Marker (Derived)
MP_MARKER_DERIVED_TYPE_KEY = 1015
# DO/Genotype
DO_GENO_TYPE_KEY = 1020
# DO/Marker (Derived)
DO_MARKER_DERIVED_TYPE_KEY = 1023


### Test Cases ###

class DerivedMarkerMPTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["rollupload"]

	def testDerivedCreationDate(self):
		"""
		Test that no source MP annotations are newer
			than the latest Derived MP annotations
		"""

		derivedDateQuery = """select creation_date 
			from voc_annot va
			where va._annottype_key = %d
			limit 1
		""" % MP_MARKER_DERIVED_TYPE_KEY
		derivedCreationDate = runQuery(derivedDateQuery)[0]['creation_date']
		
		sourceAnnotDateQuery = """select max(modification_date) as modification_date
			from voc_annot va
			where va._annottype_key = %d
		""" % MP_GENO_TYPE_KEY
		sourceModificationDate = runQuery(sourceAnnotDateQuery)[0]['modification_date']

		failMsg = "Derived MP annotations older than the latest source MP annotations"
		self.assertDataTrue(derivedCreationDate >= sourceModificationDate, failMsg)

	def testMarkerCreationDate(self):
		"""
		Test that no MP-annotated markers are newer
			than the latest Derived MP annotations
		"""

		derivedDateQuery = """select creation_date 
			from voc_annot va
			where va._annottype_key = %d
			limit 1
		""" % MP_MARKER_DERIVED_TYPE_KEY
		derivedCreationDate = runQuery(derivedDateQuery)[0]['creation_date']
		
		newMarkerDateQuery = """select max(m.creation_date) as creation_date
			from mrk_marker m
			join gxd_allelegenotype gag on
				gag._marker_key = m._marker_key
			join voc_annot va on
				va._object_key = gag._genotype_key
			where va._annottype_key = %d
		""" % MP_GENO_TYPE_KEY
		markerCreationDate = runQuery(newMarkerDateQuery)[0]['creation_date']

		failMsg = "Derived MP annotations older than latest marker with MP annotations"
		self.assertDataTrue(derivedCreationDate >= markerCreationDate, failMsg)


class DerivedMarkerDOTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["rollupload"]

	def testDerivedCreationDate(self):
		"""
		Test that no source DO annotations are newer
			than the latest Derived DO annotations
		"""

		derivedDateQuery = """select creation_date 
			from voc_annot va
			where va._annottype_key = %d
			limit 1
		""" % DO_MARKER_DERIVED_TYPE_KEY
		derivedCreationDate = runQuery(derivedDateQuery)[0]['creation_date']
		
		sourceAnnotDateQuery = """select max(modification_date) as modification_date
			from voc_annot va
			where va._annottype_key = %d
		""" % DO_GENO_TYPE_KEY
		sourceModificationDate = runQuery(sourceAnnotDateQuery)[0]['modification_date']

		failMsg = "Derived DO annotations older than the latest source DO annotations"
		self.assertDataTrue(derivedCreationDate >= sourceModificationDate, failMsg)

	def testMarkerCreationDate(self):
		"""
		Test that no DO-annotated markers are newer
			than the latest Derived MP annotations
		"""

		derivedDateQuery = """select creation_date 
			from voc_annot va
			where va._annottype_key = %d
			limit 1
		""" % DO_MARKER_DERIVED_TYPE_KEY
		derivedCreationDate = runQuery(derivedDateQuery)[0]['creation_date']
		
		newMarkerDateQuery = """select max(m.creation_date) as creation_date
			from mrk_marker m
			join gxd_allelegenotype gag on
				gag._marker_key = m._marker_key
			join voc_annot va on
				va._object_key = gag._genotype_key
			where va._annottype_key = %d
		""" % DO_GENO_TYPE_KEY
		markerCreationDate = runQuery(newMarkerDateQuery)[0]['creation_date']

		failMsg = "Derived DO annotations older than latest marker with DO annotations"
		self.assertDataTrue(derivedCreationDate >= markerCreationDate, failMsg)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(DerivedMarkerMPTestCase))
	suite.addTest(unittest.makeSuite(DerivedMarkerDOTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
