# Tests database integrity
This product has SQL-driven tests to ensure that the database is in a correct state, by checking various indicators.
Obvious corrections are reported at the end of a failed test run (e.g. which cache loads need to be rerun), to inform us how to repair the database state.

## Test Public Release

Run
    ./testPublicRelease
to ensure that MGD is ready for public release.

# Test Writing Guide
All tests go in the **tests** directory (e.g. tests/new\_module\_test.py).

A proper test case file should look like this: 

    import unittest
    from datatest import DataTestCase
    
    class NewTestCase(unittest.TestCase, DataTestCase):
    
       cacheLoads = ['newcacheload']
    
       def newSQLTest(self):
          """What the test does"""
          
          query = "select ... from ... where not exists (...)"
          self.assertQueryCount(0, query) 
    
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(NewTestCase))
        return suite
    
    
    if __name__ == '__main__':
        unittest.main()
        
Note that there are provided **assert** methods in the DataTestCase class. Use these in your tests so we can catch failures and report which _cacheLoads_ need to be re-run.

    E.g.
    self.assertQueryCount(expectedCount, query)
    self.assertDataEquals(expected, actual)
    self.assertDataTrue(booleanValue)

Next you need to update the following files:

    tests/__init__.py --->
    #Add module to __add__ list
    __add__ = [...
        "new_module_test",
    ...]

    testPublicRelease --->
    #Add to master_suite
    def master_suite():
        ...
        suites.append(new_module_test.suite())
        ...

