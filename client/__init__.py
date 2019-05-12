from controller.CDatabase import *
from controller.CClient import *

from controller.CModel import *



ans = input("What do you want ?\n 1. Train\n 2. Test\n 3. Predict one\n~> ")
if(ans == "1"):
    CModel(mode=1)
elif(ans == "2"):
    CModel(mode=2)
elif(ans == "3"):
    CModel(mode=3)
else:
    exit()
