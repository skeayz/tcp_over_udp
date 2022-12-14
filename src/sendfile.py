import socket
import math
from time import sleep
from utils import *
import threading
import datetime
import os
class sendfile:

    lastAck = 0
    duplicates = -1
    window_size = 1
    window_print = 1
    seq = 1
    transfer = True
    final_ack=0
    rtt = 0.0
    lock = threading.Lock()
    buffersize = 1494
    ss_tresh = 10000000
    last_duplicates = 0

    def __init__(self, socket, rtt):
        self.s = socket
        self.rtt = round(rtt * 1.3, 4)
        self.s.settimeout(round(rtt *5, 4))

    def receive(self):
        ack = -1
        time_window = []
        start = datetime.datetime.now()
        while True:
            # flush the buffer
            time_window.append((datetime.datetime.now() - start, self.window_print))
            try:
                data, addr = self.s.recvfrom(1024)
                print("[+] Reiceved : "+ str(custom_decode(data)) +" from " + str(addr))
                ack = int(custom_decode(data).replace("ACK", ""))            
                if(ack == self.final_ack):
                    break
                if(ack > self.lastAck or ack == self.last_duplicates):
                    self.duplicates = 0
                
                if(ack >= self.lastAck and self.ss_tresh > self.window_size):
                    with self.lock:
                        self.window_size += (ack - self.lastAck) * 2
                        self.seq = ack + 1 if ack + 1 >= self.seq else self.seq
                        self.window_print = self.window_size
                    self.lastAck = ack
                if(ack >= self.lastAck and self.ss_tresh <= self.window_size):
                    with self.lock:
                        self.window_size = (self.window_size + 1/self.window_size)
                        self.seq = ack + 1 if ack + 1 >= self.seq else self.seq
                        self.window_print = self.window_size
                    self.lastAck = ack

                if (ack == self.lastAck and self.duplicates < 2):
                    if(self.seq != self.lastAck +1):
                        self.duplicates += 1
                if(self.duplicates >= 2):
                    print("DUPLICATES ACK FOR ACK " + str(self.lastAck))
                    with self.lock:
                        self.seq = self.lastAck + 1
                        self.window_size = 1
                        self.window_print = self.window_size
                        self.last_duplicates = self.lastAck
                    self.duplicates = 0

                
                
            except socket.error as err:
                if(self.window_size >= 1):
                    print('[-] Timeout')
                    with self.lock:
                        self.ss_tresh = (self.seq - self.lastAck) // 2 if (self.seq - self.lastAck) // 2 > 30 else 20
                        self.seq = self.seq - 1 if self.seq > 1 else 1
                        self.window_size = 1
                        self.window_print = self.window_size
                    
        ## When we receive the final ack we send end to the client
        self.s.sendto(custom_encode("FIN"), addr)
        print('[+] Sent : FIN to' + str(addr))
        self.window_size = 0
        self.transfer = False
        print(datetime.datetime.now() - start, self.window_print)
        with open('time_window.txt', 'w') as f:
           for time, window_size in time_window:
               f.write(str(time) + ' ' + str(window_size) + '\n') 

    def run(self):
        print(" Start of the file transfer ")
        data, addr = self.s.recvfrom(1024)
        print("[+] Reiceved : "+ str(custom_decode(data)) +" from " + str(addr))
        try:
            f = open(custom_decode(data), 'rb')
        except FileNotFoundError:
            raise Exception("File not found")
        f.seek(0, os.SEEK_END)
        self.final_ack = math.ceil(f.tell()/self.buffersize)
        th1 = threading.Thread(target=self.receive)
        th1.start()
        # start timer
        # Send the file the client expects data messages that start with a sequence number, in string format, over 6 bytes, buffer is 1024 bytess
        while self.transfer:
            while self.window_size > 0:
                sleep(self.rtt)
                with self.lock:
                    f.seek((self.seq-1)*self.buffersize)
                    sendseq = str(self.seq).zfill(6)
                    if(self.duplicates == 0):
                        self.seq += 1
                        self.window_size -= 1     
                data = f.read(self.buffersize)
                if(data):
                    self.s.sendto(sendseq.encode() + data, addr)
                    print('\t[+] Sent : '+sendseq+' to '+ str(addr) +' with window size '+str(self.window_size))
                        
        # print time_window into a file
        th1.join()
        exit(0)   
