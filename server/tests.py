import unittest
from model.MData import *
from utils.Config import *
from controller.CData import *
import os


class TestData(unittest.TestCase):
    config = Config(file="test.ini")

    def createData(self):
        data = MData("1","2","25","1::2::25")
        self.assertEqual(data.__str__()[:18], "1::temperature::25")

    def handleData(self):
        data = CData("1::1::100")
        self.assertEqual(data.__str__()[:22],"1::luminosity::100.0::")
        self.assertFalse(data.isSuspicious())
        data = CData("a1::1::80000")
        self.assertTrue(data.isSuspicious())
    
    def getConfig(self):
        self.config.reset()
        lum = self.config.get("sensors","luminosity")
        self.assertEqual([0,1000],lum)

test = TestData()

try:
    test.createData()
    test.getConfig()
    test.handleData()
    print("All tests were successful")
    os.remove("test.ini")
except Exception as e:
    print(e)




