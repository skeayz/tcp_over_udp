def custom_decode(data : bytes) -> str:
    return data.replace(b'\x00', b'').decode()

def custom_encode(data : str) -> bytes:
    return data.encode() + b'\x00'