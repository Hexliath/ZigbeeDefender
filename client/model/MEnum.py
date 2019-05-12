from enum import Enum 

class Day(Enum):
    mon = 1
    tue = 2
    wed = 3
    thu = 4
    fri = 5
    sat = 6
    sun = 7
    @staticmethod
    def from_str(label):
        if label == "mon":
            return Day.mon
        elif label == "tue":
            return Day.tue
        elif label == "wed":
            return Day.wed
        elif label == "thu":
            return Day.thu
        elif label == "fri":
            return Day.fri
        elif label == "sat":
            return Day.sat
        elif label == "sun":
            return Day.sun
        else:
            raise NotImplementedError

class SensorType(Enum):
    luminosity = 1
    temperature = 2
    presence = 3
    @staticmethod
    def from_str(label):
        if label == "luminosity":
            return SensorType.luminosity
        elif label == "temperature":
            return SensorType.temperature
        elif label == "presence":
            return SensorType.presence
        else:
            raise NotImplementedError
            
class Suspicious(Enum):
    SUSPICIOUS = True
    NORMAL = False