import sys
import socket
import threading

from threeway import *
from utils import *
from sendfile import *

port : int
three_way_socket : socket.socket
comm_socket : socket.socket

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print(f'{"Usage: python main.py <portNumber>"}')
        exit(1)
        
    port = int(sys.argv[1])
    if(port < 1000 or port > 9999):
        print(f'{"Port number must be between 1024 and 65535"}')
        exit(1)
    
    print(f'{" Start of the TCP over UDP server on port  %d "%port:=^80}\n')

    try:
        three_way_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        three_way_socket.bind(("", port))
    except socket.error as e:
        print(f'{"Error while creating the socket"}\n')
        print(e)
        exit(1)
    
    while True:
        print(f'{" Creation of the socket ":=^80}\n')
        thr = threeway(three_way_socket, port)
        comm_socket : socket.socket = thr.run()
        
        sndf = sendfile(comm_socket)
        t1 = threading.Thread(target=sndf.run)
        t1.start()
    
    
    