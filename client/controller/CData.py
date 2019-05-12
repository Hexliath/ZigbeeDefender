from model.MData import *
from model.MEnum import *
from utils.Config import *
from controller.CDatabase import *
from controller.CModel import *
import pandas as pd



class CData:
    data = None
    flags = None

    def __str__(self):
        return self.data.__str__() + " [t:{},v:{},d:{},f:{},s:{},d:{}]".format(
            self.display(self.flags['time'][1]),
            self.display(self.flags['value'][1]),
            self.display(self.flags['date'][1]),
            self.display(self.flags['format'][1]),
            self.display(self.flags['sensor'][1]),
            self.display(self.flags['device'][1])
        ) + " " + str(self.suspicionScore()) + "% " + Suspicious(self.isSuspicious()).name + " " + self.data.original.replace("\n","")


    def __init__(self):
        pass

    def receive(self):
        db = CDatabase()
        inputs  = db.pd_select("SELECT * FROM inputs")   
        print(inputs)


