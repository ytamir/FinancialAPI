import unittest


class MachineLearningLayoutUnitTests(unittest.TestCase):
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEARDOWN")

    def testOne(self):
        self.assertEqual(True, True, "test")
