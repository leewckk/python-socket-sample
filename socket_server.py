
import logging
import threading
import socket 
import signal
import select

logging.basicConfig(level=logging.INFO)

class SocketServer:
    
    def __init__(self, bind_ip : str, bind_port: str) -> None:
        
        self._bind_ip = bind_ip
        self._bind_port = bind_port
        self._stop = False
        
        
    def handle_client(self, client_socket: socket.socket):
        
        with client_socket:
            # logging.info(f"Connecting to socket {client_socket.getpeername()}")
            
            while self._stop is not True:
                
                data = client_socket.recv(1024)
                if not data: 
                    break

                logging.info("Received %d bytes from socket, details: %s" % (len(data), data.decode("utf-8")))
        
        
    def startup(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            
            server_socket.bind((self._bind_ip, self._bind_port))
            server_socket.listen()
            
            logging.info("startup socket server bind ip: %s, port: %d " %  (self._bind_ip, self._bind_port))
            
            while self._stop is not True:
                try:

                    readable, _, _ = select.select([server_socket], [], [], 1.0)
                    for s in readable:
                        client_socket, addr = s.accept() 
                        client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                        client_thread.start()
            
                except OSError as e:
                    logging.error(e)
                    break
            
    def stop(self):
        self._stop = True
                

# def system_signal_handler(signal_number, frame):
#     logging.info("received signal number %d from signal handler" % signal_number)
                   
                
if __name__ == "__main__":
    
    server = SocketServer(bind_ip="localhost", bind_port=7788)

    def system_signal_handler(signal_number, frame):
        server.stop()
        logging.info("received system signal , number: %d, frame: %s" % (signal_number, frame))#+
        
    
    signal.signal(signal.SIGINT, system_signal_handler)
    signal.signal(signal.SIGTERM, system_signal_handler)
                
    server.startup()