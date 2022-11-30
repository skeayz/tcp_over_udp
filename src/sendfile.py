import socket
from utils import *
import threading
import datetime
import os
class sendfile:

    lastAck = 0
    duplicates = -1
    window_size = 1
    seq = 1
    transfer = True
    final_ack=0

    def __init__(self, socket: socket.socket, rtt: float):
        self.s = socket
        print("new rtt : ", round(rtt * 1.3, 4))
        self.s.settimeout(round(rtt * 1.3, 4))

    def receive(self, socket: socket.socket):
        while True:
            # flush the buffer
            try:
                data, addr = socket.recvfrom(1024)
                print(f'\t[+] Reiceved : {custom_decode(data)} from {addr}')
                ack = int(custom_decode(data).replace("ACK", ""))
                
                if(ack == self.final_ack):
                    self.s.sendto(custom_encode("FIN"), addr)
                    print(f'\t[+] Sent : FIN to {addr}')
                    break
                
                if(ack > self.lastAck):
                    self.lastAck = ack
                    self.window_size += 4
                    self.duplicates = 0

                if (ack == self.lastAck and self.duplicates < 2):
                    self.duplicates += 1
                elif (ack == self.lastAck and self.duplicates >= 2):
                    self.seq = self.lastAck
                    self.lastAck = self.lastAck-1
                    self.duplicates = 0
                    self.window_size = 1
                
            except TimeoutError as err:
                print(f'[-] Timeout')
                self.seq = self.seq - 1 if self.seq > 1 else 1
                self.window_size = 1

    def run(self):
        print(f'\t\n{" Start of the file transfer ":=^80}\n')
        data, addr = self.s.recvfrom(1024)
        print(f'\t[+] Reiceved : {custom_decode(data)} from {addr}')
        try:
            f = open(custom_decode(data), 'rb')
        except FileNotFoundError:
            raise Exception("File not found")
        f.seek(0, os.SEEK_END)
        self.final_ack = int(f.tell()/1018) + 1
        th1 = threading.Thread(target=self.receive, args=(self.s,))
        th1.start()
        time_window: list(tuple) = []
        # start timer
        start = datetime.datetime.now().timestamp()
        # Send the file the client expects data messages that start with a sequence number, in string format, over 6 bytes, buffer is 1024 bytess
        while self.transfer:
            while self.window_size > 0:
                f.seek((self.seq-1)*1018)
                data = f.read(1018)
                if(data):
                    self.s.sendto(str(self.seq).zfill(6).encode() + data, addr)
                    print(
                        f'\t[+] Sent : {str(self.seq).zfill(6)} to {addr} with window size {self.window_size}')
                    time_window.append((datetime.datetime.now().timestamp() - start, self.window_size))
                    self.seq += 1
                self.window_size -= 1
        # print time_winfow into a file
        th1.join()
        with open('time_window.txt', 'w') as f:
            for time, window_size in time_window:
                f.write(f'{time} {window_size}\n')    
        exit(0)   
