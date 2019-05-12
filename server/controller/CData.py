from model.MData import *
from model.MEnum import *
from utils.Config import *
from controller.CDatabase import *


class CData:
    data = None

    flags = {
    "time":[5, False],
    "radius":[5,False],
    "counter":[5,False],
    "pan_id":[5,False],
    "mac":[5,False],
    "encryption":[5,False],
    "value":[10, False],
    "date": [5, False],
    "format":[50, False],
    "sensor":[20, False],
    "device":[10,False]
    }


    def __str__(self):
        return str(self.data) + "\n[ma:{}, co:{}, pa:{},en:{}, ra:{}, ti:{},va:{},da:{},fo:{},se:{},de:{}]".format(
            self.display(self.flags['mac'][1]),
            self.display(self.flags['counter'][1]),
            self.display(self.flags['pan_id'][1]),
            self.display(self.flags['encryption'][1]),
            self.display(self.flags['radius'][1]),
            self.display(self.flags['time'][1]),
            self.display(self.flags['value'][1]),
            self.display(self.flags['date'][1]),
            self.display(self.flags['format'][1]),
            self.display(self.flags['sensor'][1]),
            self.display(self.flags['device'][1])
        ) + " " + str(self.suspicionScore()) + "% " + Suspicious(self.isSuspicious()).name


    @staticmethod
    def display(value):
        if value:
            return "✓"
        else:
            return "☓"

    def suspicionScore(self):
        score = 0
        for key, value in self.flags.items():
            if(value[1]):
                score += value[0]
        return score
    
    def isSuspicious(self):
        if(self.suspicionScore() >= 20):
            return True
        return False


    def __init__(self, input, attack=False):
        
        self.attack = attack
        data = self.split(input)
       
        if data is not None:
            source, destination,\
            pan_id,encryption,\
            radius, zbee_counter,\
            frame_counter, device,\
            values = self.verify(data)
            self.data = MData(device, values, input,
             source, destination, pan_id, 
             encryption, radius, zbee_counter, frame_counter)
        else:
            self.data = MData(original=input)
        
        if(attack):
            self.data.datetime['day']= data[-2]
            self.data.datetime['hours']= data[-4]
            self.data.datetime['minutes']= data[-3]
            self.data.datetime['month']= data[-1]

        print(self.data)

        self.send()


    def send(self):
        db = CDatabase()
    
        # Create one entry per sensor/value couple.
        for value in self.data.values:
            if self.attack:
                db.insert("""
            insert into `inputs` (`original`,`device`,`radius`, `zbee_counter`, `pan_id`, `frame_counter`, `source`, `destination`,
            `encryption`,`value`,`sensor`,`day`,`hours`,`minutes`,`month`,`result`) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{})
            """.format(
                self.data.original, 
                    self.data.device,
                    self.data.radius,
                    self.data.zbee_counter,
                    self.data.pan_id,
                    self.data.frame_counter,
                    self.data.source,
                    self.data.destination,
                    self.data.encryption,
                    value[1],
                    value[0].value,
                    self.data.datetime['day'],
                    self.data.datetime['hours'], 
                    self.data.datetime['minutes'], 
                    self.data.datetime['month'],
                    1
            ))

            else:

                db.insert("""
                insert into `inputs` (`original`,`device`,`radius`, `zbee_counter`, `pan_id`, `frame_counter`, `source`, `destination`,
                `encryption`,`value`,`sensor`,`day`,`hours`,`minutes`,`month`,`result`) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{})
                """.format(
                    self.data.original, 
                        self.data.device,
                        self.data.radius,
                        self.data.zbee_counter,
                        self.data.pan_id,
                        self.data.frame_counter,
                        self.data.source,
                        self.data.destination,
                        self.data.encryption,
                        value[1],
                        value[0].value,
                        self.data.datetime['day'].value,
                        self.data.datetime['hours'], 
                        self.data.datetime['minutes'], 
                        self.data.datetime['month'],
                        self.isSuspicious()
                ))
            


    def split(self, string):
        try:
            # Verify if the general format is respected.
            return string.split("::")        
        except Exception as e:
            print(e)
            self.flags["format"][1] = True
            pass
        return None


    def verify(self,values):
        if(self.attack):
            values = values[:-3]
        sensors_quantity = (len(values) - 9)/2

        """try:
            # If one field is missing, raise a warning
            if(len(values) < 10 or (sensors_quantity%1) != 0):
                raise OverflowError

        except OverflowError:
            self.flags["format"][1] = True
            pass"""

        try:
            # Verify MAC address source
            if len(values[0]) != 16:
                raise OverflowError   
        except OverflowError:
            self.flags["mac"][1] = True
            pass


        try:
            # Verify MAC address destination
            if len(values[1]) != 16:
                raise OverflowError
        except OverflowError:
            self.flags["mac"][1] = True
            pass
        
        try:
            # Verify if the device is correct
            int(values[7]) 
        except:
            #print("Error with device ID " + e)
            self.flags["device"][1] = True
            pass

        sensors_values = []
        i = 8
        while i < 8+(sensors_quantity*2):
            val = []
            try:
                # Verify if the sensor exists
                val.append(SensorType(int(values[i])))
            except:
                self.flags['sensor'][1] = True
                pass
            i += 1
            try:
                c = Config() # Value
                for key in c.getSectionKeys("sensors"):
                    if(SensorType.from_str(key) ==  SensorType(int(values[i-1]))): 
                        sensor_range = c.get("sensors",key)
                        val.append(float(values[i]))
                        if(float(values[i]) < sensor_range[0] or  float(values[i]) > sensor_range[1]):
                            raise OverflowError                           
                        break                       
            except Exception as e:
                print(e)
                self.flags["value"][1] = True
                pass
            sensors_values.append(val)
            i+=1
        
        values[8] = sensors_values
        values = values[:9]
        return values


