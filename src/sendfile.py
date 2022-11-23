class sendfile:
    
    def __init__(self, socket):
        self.s = socket
        
    def send_file(self, file):
        with open(file, 'rb') as f:
            self