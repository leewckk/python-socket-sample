import logging
import socket 
import time


class SocketClient:
    
    
    def __init__(self, dest_ip, dest_port):
        
        self._dest_ip = dest_ip
        self._dest_port = dest_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self._socket.connect((self._dest_ip, self._dest_port))
        
    def send(self, data:bytes) -> None:
        self._socket.sendall(data)

        
if __name__ == "__main__":
    
    for i in range(0, 10000):
        client = SocketClient("127.0.0.1", 7788)
        client.connect()
        client.send("hello world".encode("utf-8"))
    
    