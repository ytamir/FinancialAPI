import xmlrunner
import unittest

loader = unittest.TestLoader()
suite_one = loader.discover('UnitTests\\ConfigFilesTests')
loader = unittest.TestLoader()
suite_two = loader.discover('UnitTests\\PageCallbacksTests')
loader = unittest.TestLoader()
suite_three = loader.discover('UnitTests\\PythonRequestFileTests')
suite_all = unittest.TestSuite([suite_one, suite_two, suite_three])
runner = xmlrunner.XMLTestRunner(
                output="TestResults")
runner.run(suite_all)