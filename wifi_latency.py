# wifi_latency.py
# Billy Kihei (c) 2022
# Intelligent Mobile Device Lab @ Kennesaw State University
# Part of the wireless latency tools.

# This app measures the one-way Layer 7 delay to send bytes to a device over wi-fi.
# The purpose of this app is to measure the Layer 7 one-way delay (end-to-end) from this phone to the other phone via wifi.
# A->Wi-Fi->B, this is not an echo or RTT measurement. You will need to have a common clock observering device to be able to measure the one-way delay.

# The intended use is to run this app in Termux. This is not a standalone app.
# Provide the number of times you would like to run this application.

# 1. Open Termux.
# 2. Download the wireless_latency_tools git repo.
# 3. python wifi_latency.py <a|b> <pktsize> <#ofpackets> <IPaddress>
# 4. Example: python wifi_latency.py a 1 100 192.168.0.2 192.168.0.4, means: login as user A (192.168.0.2), send 1 byte 100 times to B (192.168.0.4)
# 5. Example: python wifi_latency.py b 1 100 192.168.0.4 192.168.0.2, means: login as user B, get one-hundred packets of size one byte from A

import socket
import sys
import signal
import time
import json
import threading
import random
import string

if len(sys.argv) == 6:
    username = sys.argv[1] # can only be a or b
    pktsize = int(sys.argv[2])
    NumTimesToRun = int(sys.argv[3])
    myIP = sys.argv[4]
    remoteIP = sys.argv[5]
elif sys.argv[1]=='a':
    print('Not enough arguments for user A, \nusage: python wifi_latency.py <a|b> <pktsize> <#ofpackets>')
    sys.exit(0)
else:
    username = sys.argv[1] # you are B

pktnumber = 0

udpClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 14400  # The port used by the TCP server
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect((HOST, PORT))

def signal_handler(sig, frame):
    udpClientSock.close()
    print('\n')
    print("%d pkts\n" % (pktnumber))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if username == 'b':
  UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  UDPServerSocket.bind((myIP, 5000))

# Device 1 is A
if username == 'a':
    print("Ensure b displays \"Listening for packets...\" then when ready...")
    x=input("Press any key to begin one-way latency test...")
    while True:
        print('Sending Packets')
        pktnumber = 0
        while (pktnumber < NumTimesToRun):
            s = ''.join(random.choice(string.digits) for _ in range(pktsize))
            udpClientSock.sendto(s.encode(), (remoteIP,5000))
            tcp_client_socket.sendall("1".encode())
            print("Sent Pkt #%d" % (pktnumber+1))
            time.sleep(1)
            udpClientSock.sendto("0".encode(), (remoteIP,5000))
            tcp_client_socket.sendall("0".encode())
            time.sleep(1)
            pktnumber += 1
            continue

# Device 2 is B
elif username == 'b':
    print("WARNING: Ensure you have b connected to an observation system. This is not a stand-alone app!")
    print("WARNING: Ensure b shows: \"Listening for packets...\", before running a")
    x=input("Press any key to receiving packets...")
    print('Listening for packets...')
    while True:
        data, client_addr = UDPServerSocket.recvfrom(pktsize)
        if data.decode()=='0':
           tcp_client_socket.sendall(data)
           print('0')
        else:
          tcp_client_socket.sendall("1".encode())
          print('1')
        pktnumber += 1
