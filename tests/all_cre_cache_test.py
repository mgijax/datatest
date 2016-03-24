"""
Test the allele cre cache load
"""

import unittest
from datatest import DataTestCase, runQuery


class AlleleCombinationTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["allcacheload.allelecrecache"]


	def testDataExists(self):
		"""
		Test that count of  ALL_Cre_Cache is non-zero
			and is equal to or greater than the count
			of recombinase results in GXD_Expression.
			(The reason the count is likely higher is because
			  the cre cache duplicates rows with multiple 
			  systems)
		"""

		creCacheCountQuery = """select count(*) cnt from all_cre_cache"""
                creCacheCount = runQuery(creCacheCountQuery)[0]['cnt']

		# assert cache is non-empty
		self.assertDataTrue(creCacheCount, "ALL_Cre_Cache should not be empty")

		creExpressionCountQuery = """select count(*) cnt
			from gxd_expression 
			where isrecombinase = 1
		"""
		creExpressionCount = runQuery(creExpressionCountQuery)[0]['cnt']

		# assert cache has appropriate count
                failMsg = "Count of results in ALL_Cre_Cache should be greater " + \
			"than or equal to count of recombinase results in GXD_Expression"
                self.assertDataTrue(creCacheCount >= creExpressionCount, failMsg)

	def testSystemHeadersExist(self):
		"""
		Test that all rows with structures have a system label
		"""
		
		systemLabelQuery = """select 1 
			from all_cre_cache
			where _emapa_term_key is not null
			and cresystemlabel is null
		"""
		self.assertQueryCount(0, systemLabelQuery)

		
		

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(AlleleCombinationTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
