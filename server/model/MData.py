from model.MEnum import *
from time import gmtime, strftime
import datetime


class MData:
    device = 0
    value = 0
    sensor = 0
    datetime = {}
    original = ""

    
    def __init__(self, device=-1, values=-1, original=-1, source=-1, destination=-1, 
        pan_id=-1, encryption=-1, radius=-1, zbee_counter=-1, frame_counter=-1):
        self.source = source
        self.destination = destination
        self.pan_id = pan_id
        self.encryption = encryption
        self.radius = radius
        self.zbee_counter = zbee_counter
        self.frame_counter = frame_counter
        self.device = int(device)
        self.values = values
        self.setDatetime()
        self.original = original.replace("\n","")

    def get(self):
        return  { 
            "source":self.source,
            "destination":self.destination,
            "pan_id":self.pan_id,
            "encryption":self.encryption,
            "radius":self.radius,
            "zbee_counter":self.zbee_counter,
            "frame_counter":self.frame_counter,
            "device":self.device,
            "values":self.values,
            "datetime":self.datetime
            }
           
    def __str__(self):
        try:
            string = ""
            for i in self.values:
                sensor = SensorType(i[0]).name
                value = i[1]
                string += str(sensor)+"::"+str(value)+"::"
            string = string[:-2]
        except Exception as e:
            print(e)
            pass

        return  "{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}".format(
            self.source,
            self.destination,
            self.pan_id,
            self.encryption,
            self.radius,
            self.zbee_counter,
            self.frame_counter,
            self.device,
            string,
            self.datetime['hours'],
            self.datetime['minutes'],
            self.datetime['day'],
            self.datetime['month'])
        
    def setDatetime(self):
        self.datetime['day'] = Day.from_str(strftime("%a", gmtime()).lower())
        self.datetime['month'] = strftime("%m", gmtime())
        self.datetime['hours'] = datetime.datetime.now().hour
        self.datetime['minutes'] =  strftime("%M", gmtime())

