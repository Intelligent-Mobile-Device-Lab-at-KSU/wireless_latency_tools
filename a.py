import socket
import time

message = "0"
bytesToSend = message.encode()
localIP     = "127.0.0.1"
localPort   = 14400
bufferSize  = 1

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
message = bytesAddressPair[0]
address = bytesAddressPair[1]
clientMsg = "Message from Client:{}".format(message)
clientIP  = "Client IP Address:{}".format(address)
print(clientMsg)
print(clientIP)
while(True):
    print("Sent pkt")
    UDPServerSocket.sendto(bytesToSend, address)
    t = time.time()
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    elaps = (time.time() - t)*1000
    print("Rx: %s" % (bytesAddressPair[0]))
    time.sleep(.5)
