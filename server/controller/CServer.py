from controller.CInputs import *
from controller.CNotify import *
from Crypto.Cipher import AES
from time import sleep
from _thread import *
import threading 
import socket 
from base64 import b64decode

class CServer:
    print_lock = threading.Lock() 

    def __init__(self):
        a = CInputs()
        t1 = threading.Thread(target=a.getInput)
        t1.start()
        self.run()


    def changeMode(self):
         print("Mode changed !")

    def do_decrypt(self,ciphertext):
        """      while len(ciphertext) % 16 != 0:
            ciphertext = ciphertext + b"~" """
        try:
            if(len(ciphertext)) % 16 != 0:
                raise OverflowError
            obj2 = AES.new('a08120efc24743a690b3bb25a30b38f7', AES.MODE_CBC, 'This is an IV456')
            message = obj2.decrypt(ciphertext)
            message = message.decode("utf-8") 
            message = message.replace(" ","")
            message = bytes(message, encoding= 'utf-8')
            message = b64decode(message)

        except (OverflowError, UnicodeDecodeError):
            message = b"BAD_MSG"
        return message
                
    # thread fuction 
    def threaded(self,c): 
        try:
            while True: 
                data = c.recv(2048) 
                len(data)
                data = self.do_decrypt(data)
                print(data)
                if not data: 
                    print('Bye') 
                    
                    self.print_lock.release() 
                    break
                elif b"CMD::CM::" in data: 
                    self.changeMode()

                elif b"BAD_MSG" in data:
                    c.send(b"NOK\n")               
                
        
        except Exception as e:
            print(e)
            c.close() 
    
    
    def run(self): 
        try:
            host = "" 
            port = 12345
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port)) 
            print("socket binded to post", port) 
        
            # put the socket into listening mode 
            s.listen(5) 
            print("socket is listening") 
        
            # a forever loop until client wants to exit 
            while True: 
        
                # establish connection with client 
                c, addr = s.accept() 
        
                # lock acquired by client 
                self.print_lock.acquire() 
                print('Connected to :', addr[0], ':', addr[1]) 
        
                # Start a new thread and return its identifier 
                start_new_thread(self.threaded, (c,)) 
        except Exception as e:
            print(e)
            s.close() 