import unittest


class StockPriceLayoutUnitTests(unittest.TestCase):
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEARDOWN")

    def testOne(self):
        self.assertEqual(True, True, "test")
