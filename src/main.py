import sys
import socket
import threading

from threeway import *
from utils import *
from sendfile import *

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: python main.py <portNumber>")
        exit(1)
        
    port = int(sys.argv[1])
    if(port < 1000 or port > 9999):
        print("Port number must be between 1024 and 65535")
        exit(1)
    
    print(f'{" Start of the TCP over UDP server on port  %d "%port:=^80}\n')

    try:
        three_way_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        three_way_socket.bind(("", port))
    except socket.error as e:
        print("Error while creating the socket")
        print(e)
        exit(1)
    
    while True:
        print(f'{" Creation of the socket ":=^80}\n')
        thr = threeway(three_way_socket, port)
        comm_socket, rtt = thr.run()
        sndf = sendfile(comm_socket, rtt)
        t1 = threading.Thread(target=sndf.run)
        t1.start()
    
    
    