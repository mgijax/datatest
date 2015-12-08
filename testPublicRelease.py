#!/usr/local/bin/python
"""
Test plan for ensuring that database is in a valid
	state for public release

Reports any data components that fail to meet tests.
Reports possible remedies (E.g. which cache loads might need to be rerun)
"""

import sys
import unittest

from tests import *

def master_suite():
	"""
	Define which tests to run in order to test that
	database is ready for public release
	"""
	suites = []

	suites.append(derived_marker_annotations_test.suite())

	suites.append(go_annot_extension_links_test.suite())
	suites.append(go_isoform_links_test.suite())

	master_suite = unittest.TestSuite(suites)

	return master_suite


if __name__ == '__main__':

	# run test suites
	test_suite = master_suite()
	runner = unittest.TextTestRunner()
	ret = not runner.run(test_suite).wasSuccessful()
	
	# report any failures
	datatest.reportFailures()

	# return proper error code
	sys.exit(ret)
