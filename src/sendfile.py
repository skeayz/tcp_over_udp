import socket
import math
from time import sleep
from utils import *
import threading
import datetime
import os

MAX_WINDOW_SIZE = 50
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
        while ack != self.final_ack:
            time_window.append((datetime.datetime.now() - start, self.window_print))
            try:
                data, addr = self.s.recvfrom(1024)
                print("[+] Reiceved : "+ str(custom_decode(data)) +" from " + str(addr))
                ack = int(custom_decode(data).replace("ACK", ""))            
                if(ack == self.final_ack and self.duplicates == 0):
                    with self.lock:
                        self.transfer = False
                        self.window_size = 0
                    break
                if(ack > self.lastAck or ack == self.last_duplicates):
                    self.duplicates = 0
                
                if(ack >= self.lastAck):
                    if (self.ss_tresh > self.window_size):
                        window_incr = (ack - self.lastAck) * 2 if (ack - self.lastAck) * 2 > 0 else 2
                    else:
                        window_incr = (self.window_size + 1/self.window_size)
                    with self.lock:
                        self.window_size = (self.window_size + window_incr)%MAX_WINDOW_SIZE
                        self.seq = ack + 1 if ack + 1 >= self.seq else self.seq
                        self.window_print = self.window_size
                    self.lastAck = ack

                if (ack == self.lastAck and ack != self.last_duplicates):
                    if(self.seq != self.lastAck +1):
                        with self.lock:
                            self.duplicates += 1
                if(self.duplicates >= 3):
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
                        self.seq = self.lastAck + 1
                        self.window_size = 1
                        self.window_print = self.window_size
                    
        ## When we receive the final ack we send end to the client
        self.s.sendto(custom_encode("FIN"), addr)
        print('[+] Sent : FIN to' + str(addr))
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
        th1.setDaemon(True)
        th1.start()
        # start timer
        # Send the file the client expects data messages that start with a sequence number, in string format, over 6 bytes, buffer is 1024 bytess
        while self.transfer:
            while self.window_size > 0:
                sleep(self.rtt/2)
                with self.lock:
                    if(self.last_duplicates == self.lastAck):
                        f.seek((self.lastAck)*self.buffersize)
                        sendseq = str(self.lastAck+1).zfill(6)
                    else:
                        f.seek((self.seq-1)*self.buffersize)
                        sendseq = str(self.seq).zfill(6)
                        self.seq += 1
                        self.window_size -= 1 if self.window_size > 1 else 0    
                    if(self.seq >= self.final_ack + 1):
                        self.window_size = 0
                data = f.read(self.buffersize)
                if(data):
                    self.s.sendto(sendseq.encode() + data, addr)
                    print('\t[+] Sent : '+sendseq+' to '+ str(addr) +' with window size '+str(self.window_size))
        th1.join()
        exit(0)   