import socket
from utils import *
class sendfile:
    
    def __init__(self, socket: socket.socket):
        self.s = socket
        
    def send_file(self, file):
        data, addr  = self.s.recvfrom(1024)
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}')
        
        # with open(file, 'rb') as f:
        #     self