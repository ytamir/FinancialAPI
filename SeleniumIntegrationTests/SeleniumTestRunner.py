import xmlrunner
import unittest

loader = unittest.TestLoader()
suite = loader.discover('SeleniumIntegrationTests\\')
runner = xmlrunner.XMLTestRunner(
                output="TestResults")
runner.run(suite)