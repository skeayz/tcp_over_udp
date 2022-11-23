import socket

class threeway:

    def __init__(self, socket):
        self.s = socket

    def three_way_handshake(self):
        
        message  = self.s.rcvfrom(1024)
        addr  = message[1]
        message = message[0]
        print("connexion établie avec", addr)
        
        self.s.sendto("SYN".encode())
        print("SYN envoyé")
        
        message = self.s.rcvrfrom(1024)
        message = message[0]
        print(message)
        print("SYN-ACK reçu")
        
        self.s.sendto("ACK".encode())
        print("ACK envoyé")