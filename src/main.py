import sys
import socket

from threeway import *

port : int
s : socket.socket

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print(f'{"Usage: python main.py <portNumber>"}')
        exit(1)
    port = int(sys.argv[1])
    print(f'{"Port number : "}{port}')
    print(f'{" Start of the TCP over UDP server":=^80}')
    print(f'{" Creation of the socket ...":=^80}')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))
    threeway = threeway(s)
    threeway.three_way_handshake()
    