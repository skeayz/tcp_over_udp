import socket
import random
import time
from utils import *

class threeway:

    def __init__(self, socket : socket.socket, current_port : int):
        self.s = socket
        self.current_port = current_port

    def run(self) -> socket.socket:
    
        data, addr  = self.s.recvfrom(1024)
        if(custom_decode(data) != 'SYN'):
            raise Exception("SYN not received")
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}')
        
        # Create new random port greater than current port but inferior to 9999
        new_port = self.current_port + random.randint(1, 9999 - self.current_port)
        try:
            comm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            comm_socket.bind(("", new_port))
        except socket.error as e:
            print(f'{"Error while creating the socket"}\n')
            print(e)
            exit(1)
        #Create the Syn-ACk message including the new port
        synack = f"SYN-ACK{str(new_port).zfill(4)}"
        
        initial_time = time.time()
        self.s.sendto(custom_encode(synack), addr)
        print(f'[+] Sent : {synack} to {addr}')
        
        data, addr = self.s.recvfrom(1024)
        ending_time = time.time()
        
        rtt = str(ending_time - initial_time)
        print(rtt)
        
        if(custom_decode(data) != "ACK"):
            raise Exception("ACK not received")
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}')
        
        return comm_socket