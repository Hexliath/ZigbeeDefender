"""
    Zigbee frame builder

    This script contains various functions to create random or invalid frames.

    Example of a valid frame with known src :
    00:13:a2:00:41:4f:36:cd 00:13:a2:00:41:4f:37:55 0x0000b0fb 1 30 159 88623 00004198800041c666a4

    Example of a invalid frame with random src :
    91:e6:c1:23:9b:20:9d:d2 00:13:a2:00:41:4f:37:55 0x0000b0fb 0 30 159 88623 00e8c019999a472dd733
"""

import random
import math
import struct
import sys
import datetime
import time

class Frame:
    def __init__(self, src = "", dst = "0013a200414f3755", pan_id = "0000b0fb", encryption_status = 1, radius = 30,\
                zbee_counter = 0, frame_counter = 0, device_nb = 0, temperature = 1,
                temp_val = 0.0, luminosity = 2, lum_val = 0.0, date = "10::11::3::4"):
        self.src = src
        self.dst = float().fromhex(dst)
        self.pan_id = float().fromhex(pan_id)
        self.encryption_status = encryption_status
        self.radius = radius
        self.zbee_counter = zbee_counter
        self.frame_counter = frame_counter
        self.device_nb = device_nb
        self.temperature = temperature
        self.temp_val = temp_val
        self.luminosity = luminosity
        self.lum_val = lum_val
        self.date = date

    # Format a string containing all the values and print it
    def sendData(self):
        print('{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}'.format(
                    self.src,
                    self.dst,
                    self.pan_id,
                    self.encryption_status,
                    self.radius,
                    self.zbee_counter,
                    self.frame_counter,
                    self.device_nb,
                    self.temperature,
                    self.temp_val,
                    self.luminosity,
                    self.lum_val,
                    self.date), flush=True)


    # Encryption status randomizer
    def randEncryptStatus(self):
        self.encryption_status = random.randint(0,1)

    def setEncryptStatus(self, enc):
        self.encryption_status = enc

    # Source adress randomizer
    def randSrc(self):
        self.src = randhex(8,"")
        self.src = float().fromhex(self.src)

    def setSrc(self, src):
        self.src = float().fromhex(src) 

    def setDist(self, dist):
        self.dst = float().fromhex(dist)

    # Radius randomizer
    def randRadius(self):
        self.radius = random.randint(0,255)

    def setRadius(self, radius):
        self.radius = radius

    # Zbee counter randomizer
    def randZigbeeCounter(self):
        val = randhex(4,"")
        self.zbee_counter = str(struct.unpack(">I",bytes.fromhex(val))[0])

    def setZcounter(self, zcounter):
        self.zbee_counter = zcounter

    # Frame counter randomizer
    def randFrameCounter(self):
        val = randhex(4,"")
        self.frame_counter = str(struct.unpack(">I",bytes.fromhex(val))[0])

    def setFcounter(self, fcounter):
        self.frame_counter = fcounter

    # Temp value randomizer
    def randTemp(self):
        val = randhex(4,"")
        self.temp_val = str(struct.unpack("!f",bytes.fromhex(val))[0])

    # Realistic temp value randomizer
    def realRandTemp(self):
        val = random.uniform(15.0, 30.0)
        self.temp_val = truncate(val, 1)

    # Lum value randomizer
    def randLum(self):
        val = randhex(4,"")
        self.lum_val = str(struct.unpack("!f",bytes.fromhex(val))[0])

    # Realistic lum value randomizer
    def realRandLum(self):
        val = random.uniform(50.0, 500.0)
        self.lum_val = truncate(val, 1)

    # Randomize all fields with random hexadecimal values (can give totally unrealistic values)
    def randAll(self):
        self.randSrc()
        self.randEncryptStatus()
        self.randRadius()
        self.randZigbeeCounter()
        self.randFrameCounter()
        self.randLum()
        self.randTemp()

    # Randomize fields with realistic value
    def realRandAll(self):
        self.randSrc()
        self.randEncryptStatus()
        self.randRadius()
        self.randZigbeeCounter()
        self.randFrameCounter()
        self.realRandLum()
        self.realRandTemp()

    # Set all fields back to their default value
    def resetFields(self):
        self.src = ""
        self.dst = float().fromhex("0013a200414f3755")
        self.pan_id = float().fromhex("0000b0fb")
        self.encryption_status = 1
        self.radius = 30
        self.zbee_counter = 0
        self.frame_counter = 0
        self.device_nb = 0
        self.temperature = 1
        self.temp_val = 0.0
        self.luminosity = 2
        self.lum_val = 0.0
        self.date = "10::11::3::4"

    def setDate(self, date):
        if int(date.strftime("%M"))<10 : 
            self.date = date.strftime("%M")[1:] + "::"
        else : 
            self.date = date.strftime("%M") + "::"
        if int(date.strftime("%H"))<10 : 
            self.date = self.date + date.strftime("%H")[1:] + "::"
        else : 
            self.date = self.date + date.strftime("%H") + "::"
        self.date = self.date + str(date.weekday()+1) + "::"
        if int(date.strftime("%m"))<10 : 
            self.date = self.date + date.strftime("%m")[1:]
        else : 
            self.date = self.date + date.strftime("%m")


# Returns a random hex string containing a given number of caracter (multiple of 2)
def randhex(size = 1, sep = ""):
    result = []
    for i in range(size):
        result.append(str(random.choice("0123456789abcdef")) + str(random.choice("0123456789abcdef")))
    return sep.join(result)

# Trunc a float with a given digits number
def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    date = datetime.datetime(2018, 4, 20, 8, 30)
    datechg = 0
    full_rand = 0
    enc = 1
    radius = 30
    src = float().fromhex("0012b20541f47698")
    srcchg = 0
    dist = float().fromhex("0013a200414f3755")
    distchg = 0
    zcounter = 0
    zcounter_Inc = 1
    fcounter = 0
    fcounter_Inc = 1
    number = 1
    today = 0

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
                print("""
                FrameGenerator          User Commands
                DESCRIPTION :
                    create generated frames with specific randomized values 
            
                USAGE :
                    --full_rand
                        Create a full random frame with random source, 
                        random Encrypt Status, random radius, 
                        random Zigbee counter, random frame counter, 
                        random values for device ( 1 lum + 1 temp )
    
                    --encrypt
                        Specify if Encrypt status is 1 or 0, can be -1 for rand
                        default is 1
    
                    --radius
                        Specify radius, can be -1 for rand
                        default is 30

                    --src
                        Specify source adress eg: "0012b20541f47698"
                        can be -1 for rand
 
                   --dist
                        Specify destination adress eg: "0012b20541f47698"
                        default is 0013a200414f3755
 
                   --zcounter
                        Specify the start of the Zigbee counter
                        default is 0
 
                   --zcounter_Inc
                        default Zcounter value is 1 : 
                            the Zigbee Counter will be incremented by 1 each frame
                        can be also 0 :
                            the Zigbee Counter will be full randomized
 
                   --fcounter
                        Specify the start of the frame counter
 
                   --fcounter_Inc
                        default Fcounter value is 1 : 
                            the frame Counter will be incremented by 1 each frame
                        can be also 0 :
                            the frame Counter will be full randomized

                    --date
                        default date : 04:20:08:30
                        defined like : Month:day:hour:minute

                    --number
                        the number of trame who will be created
                        default is 1
    
                """)
        counter = 0
        if sys.argv.count("--src") == 0 and sys.argv.count("--full_rand") == 0:
            print("ERROR : NO --src SPECIFIED")
            sys.exit()

        for arg in sys.argv:
            counter = counter + 1
            if arg == "--full_rand":
                full_rand=1
            if arg == "--encrypt":
                if sys.argv[counter] == "0" or sys.argv[counter] == "1" or sys.argv[counter] == "-1":
                    enc = int(sys.argv[counter])
                else:
                    print("ERROR : BAD --encrypt PARAMETER")
                    sys.exit()
            if arg == "--radius":
                try :
                    radius = int(sys.argv[counter])
                except ValueError:
                    print("ERROR : BAD --radius PARAMETER")
                    sys.exit()
            if arg == "--src":
                if sys.argv[counter] == "-1":
                    srcchg = -1
                else:
                    if len(sys.argv[counter])==16:
                        src = sys.argv[counter]
                        srcchg = 1
                    else:
                        print("ERROR : BAD --src PARAMETER")
                        sys.exit()
            if arg == "--dist":
                if len(sys.argv[counter])==16:
                    dist = sys.argv[counter]
                    distchg = 1
                else:
                    print("ERROR : BAD --dist PARAMETER")
            if arg == "--zcounter":
                try :
                    zcounter = int(sys.argv[counter])
                except ValueError:
                    print("ERROR : BAD --zcounter PARAMETER")
                    sys.exit()
            if arg == "--zcounter_Inc":
                if sys.argv[counter] == "0" or sys.argv[counter] == "1":
                    zcounter_Inc=int(sys.argv[counter])
            if arg == "--fcounter":
                try :
                    fcounter = int(sys.argv[counter])
                except ValueError:
                    print("ERROR : BAD --fcounter PARAMETER")
                    sys.exit()
            if arg == "--fcounter_Inc":
                if sys.argv[counter] == "0" or sys.argv[counter] == "1":
                    fcounter_Inc=int(sys.argv[counter])
            if arg == "--date":
                if sys.argv[counter] == "today":
                    date = datetime.datetime.now()
                    today = 1
                else :
                    date = datetime.datetime(2018, int(sys.argv[counter].split(":")[0]), int(sys.argv[counter].split(":")[1]), int(sys.argv[counter].split(":")[2]), int(sys.argv[counter].split(":")[3]))
            if arg == "--number" and today == 0:
                try :
                    number = int(sys.argv[counter])
                except ValueError:
                    print("ERROR : BAD --number PARAMETER")
                    sys.exit()
    
        frame = []
        for i in range(number):
            frame.append(Frame())
            if full_rand==1:
                frame[i].randAll()
                frame[i].randSrc()
            else:
                frame[i].setRadius(radius)
                if enc==0:
                    frame[i].setEncryptStatus(0)
                if enc == -1:
                    frame[i].randEncryptStatus()
                if srcchg == 1:
                    frame[i].setSrc(src)
                if srcchg == -1:
                    frame[i].randSrc()
                if distchg == 1:
                    frame[i].setDist(dist)
                if zcounter_Inc == 1:
                    frame[i].setZcounter(zcounter)
                if zcounter_Inc == 0:
                    frame[i].randZigbeeCounter()
                if fcounter_Inc == 1:
                    frame[i].setFcounter(fcounter)
                if fcounter_Inc == 0:
                    frame[i].randFrameCounter()
                
                frame[i].realRandLum()
                frame[i].realRandTemp()
                frame[i].setDate(date)
                date = date + datetime.timedelta(seconds=30)
                zcounter = zcounter + 1
                fcounter = fcounter + 1

        i = 0
        while i in range(number):
            frame[i].sendData()
            sys.stdout.flush()
            i = i + 1
            time.sleep(2)
    else:
        frame = Frame()
        frame.randAll()
        frame.sendData()
        frame.resetFields()
        frame.realRandAll()
        frame.sendData()
