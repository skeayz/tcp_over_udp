import socket
from utils import *
class sendfile:
    
    def __init__(self, socket: socket.socket):
        self.s = socket
        
    def run(self):
        print(f'\n{" Start of the file transfer ":=^80}\n')
        data, addr  = self.s.recvfrom(1024)
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}')