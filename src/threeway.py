import socket
import random

class threeway:

    def __init__(self, socket : socket.socket, current_port : int):
        self.s = socket
        self.current_port = current_port

    def run(self) -> int:
        
        data, addr  = self.s.recvfrom(1024)
        if(custom_decode(data) != 'SYN'):
            raise Exception("SYN not received")
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}\n')
        
        # Create new random port greater than current port but inferior to 9999
        new_port = self.current_port + random.randint(1, 9999 - self.current_port)
        #Create the Syn-ACk message including the new port
        synack = f"SYN-ACK{str(new_port).zfill(4)}"
        
        self.s.sendto(synack.encode(), addr)
        print(f'[+] Sent : {synack} to {addr}\n')
        
        data, addr = self.s.recvfrom(1024)
        if(custom_decode(data) != "ACK"):
            raise Exception("ACK not received")
        print(f'[+] Reiceved : {custom_decode(data)} from {addr}\n')
        
        return new_port

def custom_decode(data : bytes) -> str:
    return data.replace(b'\x00', b'').decode()