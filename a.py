import socket
import time

serverAddressPort   = ("127.0.0.1", 4400)
bufferSize          = 1

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while(True):
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    t = time.time()
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    elapsed = time.time()-t
    print("From %s, elapsed: %d" % (msgFromServer[0].decode(),elapsed))
