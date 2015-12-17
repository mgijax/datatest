"""
Test the genotype-based allele combination
	cache loads
"""

import unittest
from datatest import DataTestCase

ALL_COMBINATION_1_TYPE_KEY = 1016
ALL_COMBINATION_2_TYPE_KEY = 1017
ALL_COMBINATION_3_TYPE_KEY = 1018


class AlleleCombinationTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["allcacheload.allelecombination"]


	def testNotesExist(self):
		"""
		Test that all genotypes have an allele combination
			note
		"""
		
		for noteTypeKey in [ALL_COMBINATION_1_TYPE_KEY, \
			ALL_COMBINATION_2_TYPE_KEY, \
			ALL_COMBINATION_3_TYPE_KEY]:
	
		    query = """
		    select 1
		    from gxd_genotype gg
		    join gxd_allelepair gap on
			    gap._genotype_key = gg._genotype_key
		    where not exists (select 1 from 
			    mgi_note mn
			    where mn._object_key = gg._genotype_key
			    and mn._notetype_key = %d
		    )
		    """ % (noteTypeKey)

		    self.assertQueryCount(0, query, msg="Genotypes missing _notetype_key = %d" % noteTypeKey)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(AlleleCombinationTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
