"""
Test the derived marker annotations (e.g. MP and OMIM)
	which come from the rollupload
"""

import unittest
from datatest import DataTestCase, runQuery

### Constants ###
# Mammalian Phenotype/Genotype
MP_GENO_TYPE_KEY = 1002
# Mammalian Phenotype/Marker (Derived)
MP_MARKER_DERIVED_TYPE_KEY = 1015
# OMIM/Genotype
OMIM_GENO_TYPE_KEY = 1005
# OMIM/Marker (Derived)
OMIM_MARKER_DERIVED_TYPE_KEY = 1016


### Test Cases ###

class DerivedMarkerMPTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["rollupload"]

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

		self.assertDataTrue(derivedCreationDate >= markerCreationDate, "Derived MP annotations older than latest marker with MP annotations")


class DerivedMarkerOMIMTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["rollupload"]

	def testMarkerCreationDate(self):
		"""
		Test that no OMIM-annotated markers are newer
			than the latest Derived MP annotations
		"""

		derivedDateQuery = """select creation_date 
			from voc_annot va
			where va._annottype_key = %d
			limit 1
		""" % OMIM_MARKER_DERIVED_TYPE_KEY
		derivedCreationDate = runQuery(derivedDateQuery)[0]['creation_date']
		
		newMarkerDateQuery = """select max(m.creation_date) as creation_date
			from mrk_marker m
			join gxd_allelegenotype gag on
				gag._marker_key = m._marker_key
			join voc_annot va on
				va._object_key = gag._genotype_key
			where va._annottype_key = %d
		""" % OMIM_GENO_TYPE_KEY
		markerCreationDate = runQuery(newMarkerDateQuery)[0]['creation_date']

		self.assertDataTrue(derivedCreationDate >= markerCreationDate, "Derived OMIM annotations older than latest marker with OMIM annotations")

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(DerivedMarkerMPTestCase))
	suite.addTest(unittest.makeSuite(DerivedMarkerOMIMTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
