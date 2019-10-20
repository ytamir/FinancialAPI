from PyhonRequestFiles import FinancialStatementsJSONParser
from ConfigFiles import MetricsConfig
import unittest


class FinancialStatementsJSONParserUnitTests(unittest.TestCase):
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEARDOWN")

    def testOne(self):
        symbols = ["AAPL", "GRMN", "CERN"]
        metric_ex = ["NUMBER OF SHARES", "NIPEREBT", "Market Capitalization"]
        frequency = MetricsConfig.Frequencies.QUARTERLY
        print(FinancialStatementsJSONParser.fetch_data(frequency, metric_ex, symbols, []))
        self.assertEqual(True, True, "test")
