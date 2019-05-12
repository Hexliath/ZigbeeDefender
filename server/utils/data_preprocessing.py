import struct
import time
import sys
from  enum import Enum
""" 
This script allows to parse the tshark output and
transform into the correct data format.
00:13:a2:00:41:4f:36:cd 00:13:a2:00:41:4f:37:55 0x0000b0fb 1 30 159 88623 00004198800041c666a4

"""
run = True

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
            

def handleInput(line):
    src, dst, pan_id, encryption_status, radius, zbee_counter, frame_counter, payload = line.split(" ")
    device_nb = payload[:3]
    temp_val = payload[4:12]
    lum_val = payload[12:]
    src = "0x" + src.replace(":","")
    dst = "0x" + dst.replace(":","")
    pan_id = float().fromhex(pan_id)
    src = float().fromhex(src)
    dst = float().fromhex(dst)
    

    print('{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}'.format(
                src,
                dst,
                pan_id,
                encryption_status,
                radius,
                zbee_counter,
                frame_counter,
                int(device_nb,16),
                SensorType.temperature.value,
                str(struct.unpack("!f",bytes.fromhex(temp_val))[0]),
                SensorType.luminosity.value,
                str(struct.unpack("!f",bytes.fromhex(lum_val))[0])
        ))

while run:
    data = ''
    line = ''
    while data != '\n':
        data = sys.stdin.read(1)
        line += data
    if line.startswith("END"):
            run = False
    else:
        handleInput(line)
        sys.stdout.flush()
