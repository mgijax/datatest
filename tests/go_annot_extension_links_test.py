"""
Test the GO annotation extension display links
	which are cache loaded as an MGI_Note 
	attached to VOC_Evidence_Property
"""

import unittest
from datatest import DataTestCase

import go_annot_extensions

# GO Annotation Extension Display Link _notetype_key
GO_ANNOT_EXT_DISPLAY_NOTETYPE_KEY = 1045

class GOAnnotExtensionLinksTestCase(unittest.TestCase, DataTestCase):
	
	cacheLoads = ["mgicacheload.go_annot_extensions_display_load"]

	def setUp(self):
		
		# Get the clauses for selecting GO
		# annotation extensions

		extensionProcessor = go_annot_extensions.Processor()
		propertyTermKeys = extensionProcessor.querySanctionedPropertyTermKeys()
		evidenceTermKeys = extensionProcessor.querySanctionedEvidenceTermKeys()

		self.propertyKeyClause = ",".join([str(k) for k in propertyTermKeys])
		self.evidenceKeyClause = ",".join([str(k) for k in evidenceTermKeys])

	def testNotesExist(self):
		"""
		Test that all annotation extensions have
		    a display link note
		"""

		query = """
		select 1 
		from voc_evidence ve 
		join voc_evidence_property vep on
			vep._annotevidence_key = ve._annotevidence_key
		where ve._evidenceterm_key in (%s)
		and vep._propertyterm_key in (%s)
		and not exists (select 1 from
			mgi_note mn 
			where mn._object_key = vep._evidenceproperty_key
			and mn._notetype_key = %d
		)
		""" % (self.evidenceKeyClause, self.propertyKeyClause,
			GO_ANNOT_EXT_DISPLAY_NOTETYPE_KEY)

		self.assertQueryCount(0, query)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(GOAnnotExtensionLinksTestCase))
	return suite


if __name__ == '__main__':
	unittest.main()
