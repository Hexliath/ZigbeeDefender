from time import sleep
from _thread import *
import threading 
import socket 
from base64 import b64decode


class CClient:
    
    def __init__(self):
        pass
        
    def createModel(self, name=None):
        model = CModel(name)
    
