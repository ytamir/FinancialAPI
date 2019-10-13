from selenium import webdriver
import unittest


class MachineLearningPageSeleniumTests(unittest.TestCase):
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEARDOWN")

    def testOne(self):
        path = "SeleniumIntegrationTests\\chromedriver.exe"
        print(path)
        print("here")
        driver = webdriver.Chrome(path)
        driver.get("http://ytamir.xyz/")
        driver.close()