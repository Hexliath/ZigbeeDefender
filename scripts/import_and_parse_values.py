import numpy as np
from enum import Enum
import tensorflow as tf
import pandas as pd

class Location(Enum):
    LIVING_ROOM = 1
    KITCHEN = 2
    BEDROOM = 3

class SensorType(Enum):
    luminosity = 1
    temperature = 2
    @staticmethod
    def from_str(label):
        if label == "luminosity":
            return SensorType.luminosity
        elif label == "temperature":
            return SensorType.temperature
        else:
            raise NotImplementedError

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
        else:
            raise NotImplementedError


class Data:
    list_values = []
    def __init__(self,input):
        self.process_input(input)

    def process_input(self, input):
        for entry in input:
            self.strip_value(entry)


    def strip_value(self, input):
        """ Parse the string and create dictionnary """
        values = input.split("::")
        dict = {}
        try:
            dict['sensor'] = SensorType.from_str(values[0]).value
            dict['value'] = int(values[1])
            dict['place'] = int(values[2])
            dict['hour'] = int(values[3])
            dict['minutes'] = int(values[4])
            dict['day'] = Day.from_str(values[5]).value
            dict['month'] = int(values[6])
            self.list_values.append(dict)
        except NotImplementedError:
            print("Incorrect value found from input " + "[{}]".format(values[0]))

    def __repr__(self):
        values = ""
        for value in self.list_values:
            values += ", " + str(value)
        return values[1:]


    def get(self):
        """ Return a dataframe with all data"""
        df = pd.DataFrame.from_dict(self.list_values[0], orient="index").T

        for i in range(len(self.list_values)):
            df.loc[i] = list(self.list_values[i].values())

        return df



test = Data(["luminosity::358::4::14::06::wed::01",
"temperature::34::4::14::09::wed::01",
"presence::34::4::14::09::wed::01",
"test::34::4::14::09::wed::01",
"temperature::38::4::14::09::wed::01"
]).get()



print(test)
