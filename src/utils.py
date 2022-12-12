def custom_decode(data) :
    return data.replace(b'\x00', b'').decode()

def custom_encode(data):
    return data.encode() + b'\x00'