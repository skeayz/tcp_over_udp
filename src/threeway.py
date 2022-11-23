import socket

class threeway:

    def __init__(self, socket):
        self.s = socket

    def three_way_handshake(self):
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print("connexion établie avec", self.addr)
        self.conn.send("SYN".encode())
        print("SYN envoyé")
        self.conn.recv(1024)
        print("SYN-ACK reçu")
        self.conn.send("ACK".encode())
        print("ACK envoyé")