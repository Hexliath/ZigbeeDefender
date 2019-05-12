import sys
from controller.CData import *
from utils.Config import *

class CInputs:
    def getInput(self):
        do_run = True
        while do_run:
            i = ''
            line = ''
            while i != '\n':   # read one char at a time until RETURN
                i = sys.stdin.read(1)
                line += i
            #                                   
            if line.startswith("END"):
                do_run = False
            else:
                self.handleInput(line)
                sys.stdout.flush()
                
    def handleInput(self,line):
        c = Config()
        if c.get("model","mode") == "TRAIN":
            print("Training")
            new_input = CData(line)
        if c.get("model","mode") == "ATTACK":
            print("Attack")
            new_input = CData(line,attack=True)
        elif c.get("model","mode") == "ENGAGED":
            print("Model engaged")
        else:
            print("Current mode not supported")
        print(new_input)