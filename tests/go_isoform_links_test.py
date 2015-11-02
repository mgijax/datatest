"""
Test the GO Isoform display links
	which are cache loaded as an MGI_Note 
	attached to VOC_Evidence_Property
"""

import unittest
from datatest import DataTestCase

import go_isoforms

# GO Isoform Display Link _notetype_key
GO_ISOFORM_DISPLAY_NOTETYPE_KEY = 1046

class GOIsoformLinksTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["mgicacheload.go_isoforms_display_load"]

	def setUp(self):
		
		# Get the clauses for selecting GO
		# Isoforms

		isoformProcessor = go_isoforms.Processor()
		propertyTermKeys = isoformProcessor.querySanctionedPropertyTermKeys()

		self.propertyKeyClause = ",".join([str(k) for k in propertyTermKeys])

	def testNotesExist(self):
		"""
		Test that all isoforms have
		    a display link note
		"""

		query = """
		select 1 
		from voc_evidence ve 
		join voc_evidence_property vep on
			vep._annotevidence_key = ve._annotevidence_key
		where vep._propertyterm_key in (%s)
		and not exists (select 1 from
			mgi_note mn 
			where mn._object_key = vep._evidenceproperty_key
			and mn._notetype_key = %d
		)
		""" % (self.propertyKeyClause,
			GO_ISOFORM_DISPLAY_NOTETYPE_KEY)

		self.assertQueryCount(0, query)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(GOIsoformLinksTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
