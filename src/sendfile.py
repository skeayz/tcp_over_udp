import socket
class sendfile:
    
    def __init__(self, socket: socket.socket):
        self.s = socket
        
    def send_file(self, file):
        with open(file, 'rb') as f:
            self