"""
datatest classes
"""
import logging
import os

import db

### Globals ###
# Track test failures
FAILURES = []
CACHELOADS = set([])

### initialize database settings ###
db.set_sqlUser('mgd_public')
db.set_sqlPassword('mgdpub')
db.set_sqlServer( os.environ['DATATEST_DBSERVER'] )
db.set_sqlDatabase( os.environ['DATATEST_DBNAME'] )

### Classes ###

class DataTestCase(object):
	"""
	datatest Test Case
	Exposes special assertion methods

	Tracks and reports failures
	"""

	def __init__(self):

		# Ensure that subclass has implemented the cacheLoads attribute
		#	for tracking which cacheLoads the tested data is dependent on

		if not hasattr('cacheLoads', self):
			errMsg = self.__class__ + " does not implement 'cacheLoads' attribute"
			raise NotImplementedError(errMsg)


	def assertQueryCount(self, count, query, msg=None):
		"""
		Assert that the query returns count number of results
		"""
		results = runQuery(query)
		
		try:
			self.assertEquals(count, len(results), msg)
		except AssertionError, ae:
			self._recordAssertionFailure()
			raise

	def assertDataEquals(self, expected, actual, msg=None):
		"""
		Assert equals wrapper
		"""
		try:
			self.assertEquals(expected, actual, msg)
		except AssertionError, ae:
			self._recordAssertionFailure()
			raise

	def assertDataTrue(self, booleanValue, msg=None):
		"""
		AssertTrue wrapper
		"""
		try:
			self.assertTrue(booleanValue, msg)
		except AssertionError, ae:
			self._recordAssertionFailure()
			raise
		
	def _recordAssertionFailure(self):
		global CACHELOADS
		CACHELOADS.update(self.cacheLoads)


### methods ###

def runQuery(query):
	return db.sql(query, 'auto')


def log(msg):
	print msg

def reportFailures():
	"""
	Report any test failures
	"""
	if CACHELOADS:

		msg = """The following cache loads may need to be rerun:\n"""

		cacheloads = list(CACHELOADS)
		cacheloads.sort()
		for cacheload in cacheloads:
			msg += "\t" + cacheload + "\n"

		log(msg)
