import socket
from utils import *
import threading
class sendfile:
    
    lastAck = 0
    duplicates = -1
    window_size = 1
    
    def __init__(self, socket: socket.socket):
        self.s = socket
    
    def receive(self, socket: socket.socket):
        while True:
            data, addr = socket.recvfrom(1024)
            print(f'\t[+] Reiceved : {custom_decode(data)} from {addr}')
            ack = int(custom_decode(data).replace("ACK", ""))
            if(ack == self.lastAck):
                self.duplicates = ack + 1
            self.lastAck = ack
        
    def run(self):
        print(f'\t\n{" Start of the file transfer ":=^80}\n')
        data, addr  = self.s.recvfrom(1024)
        print(f'\t[+] Reiceved : {custom_decode(data)} from {addr}')
        th1 = threading.Thread(target=self.receive, args=(self.s,))
        th1.start()
        #check if file exists
        try:
            f = open(custom_decode(data), 'rb')
        except FileNotFoundError:
            raise Exception("File not found")
        #Send the file the client expects data messages that start with a sequence number, in string format, over 6 bytes, buffer is 1024 bytes
        seq = 1
        while True:
            if self.duplicates != -1:
                seq = self.duplicates
                self.duplicates = -1
            f.seek((seq-1)*1018)
            data = f.read(1018)
            if(data):
                self.s.sendto(str(seq).zfill(6).encode() + data, addr)
                print(f'\t[+] Sent : {str(seq).zfill(6)} to {addr}')
                seq += 1
            else:
                break
        f.close()
        print(f'{" End of the file transfer ":=^80}\n')
        