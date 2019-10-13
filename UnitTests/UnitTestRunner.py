import xmlrunner
import unittest

loader = unittest.TestLoader()
suite_one = loader.discover('.\\ConfigFilesTests')
loader = unittest.TestLoader()
suite_two = loader.discover('.\\PageCallbacksTests')
loader = unittest.TestLoader()
suite_three = loader.discover('.\\PageLayoutsTests')
loader = unittest.TestLoader()
suite_four = loader.discover('.\\PythonRequestFileTests')
suite_all = unittest.TestSuite([suite_one, suite_two, suite_three, suite_four])
runner = xmlrunner.XMLTestRunner(
                output=".\\TestResults")
runner.run(suite_all)