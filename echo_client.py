# echo-client.py
import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 14400  # The port used by the server

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect((HOST, PORT))
while 1:
    tcp_client_socket.sendall(b"Hello, world")
    data = tcp_client_socket.recv(1024)
    print(f"Received {data!r}")
    time.sleep(1)
