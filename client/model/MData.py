from model.MEnum import *
from time import gmtime, strftime

class MData:
    device = 0
    value = 0
    sensor = 0
    datetime = {}
    original = ""

    def __init__(self, device, sensor, value, original):
        self.device = int(device)
        self.sensor = int(sensor)
        self.value = float(value)
        self.setDatetime()
        self.original = original.replace("\n","")

    def get(self):
        return  { "device":self.device,
            "sensor":self.sensor,
            "value":self.value,
            "datetime":self.datetime}
           
    def __str__(self):
        try:
            sensor = SensorType(self.sensor).name
        except:
            sensor = self.sensor
        return  "{}::{}::{}::{}::{}::{}::{}".format(
            self.device,
            sensor,
            self.value,
            self.datetime['hours'],
            self.datetime['minutes'],
            Day(self.datetime['day']).name,
            self.datetime['month'])
         

    def setDatetime(self):
        self.datetime['day'] = Day.from_str(strftime("%a", gmtime()).lower())
        self.datetime['month'] = strftime("%m", gmtime())
        self.datetime['hours'] =  strftime("%H", gmtime())
        self.datetime['minutes'] =  strftime("%M", gmtime())
