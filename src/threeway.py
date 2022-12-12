import socket
import random
import time
from utils import *

class threeway:

    def __init__(self, socket, current_port):
        self.s = socket
        self.current_port = current_port

    def run(self):
    
        data, addr  = self.s.recvfrom(1024)
        if(custom_decode(data) != 'SYN'):
            raise Exception("SYN not received")
        print("[+] Reiceved : " + str(custom_decode(data)) + " from " + str(addr))
        
        # Create new random port greater than current port but inferior to 9999
        new_port = self.current_port + random.randint(1, 9999 - self.current_port)
        try:
            comm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            comm_socket.bind(("", new_port))
        except socket.error as e:
            print("Error while creating the socket")
            print(e)
            exit(1)
        #Create the Syn-ACk message including the new port
        synack = f"SYN-ACK{str(new_port).zfill(4)}"
        
        initial_time = time.time()
        self.s.sendto(custom_encode(synack), addr)
        print("[+] Sent : synack to " + str(addr))
        
        data, addr = self.s.recvfrom(1024)
        ending_time = time.time()
        
        rtt = float(ending_time - initial_time)
        
        if(custom_decode(data) != "ACK"):
            raise Exception("ACK not received")
        print("[+] Reiceved : " + str(custom_decode(data)) + "from " + str(addr))
        
        return (comm_socket, rtt)