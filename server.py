#!/usr/bin/env python3


from socket import *
import select
import sys
import os
import pickle
from datetime import datetime


def log(client, time, request, status):
    os.chdir(cwd)
    log = open("server.log", "a+")
    log.write(str(client[0]) + ":" + str(client[1]) + "    " + time + "    " + request + "    " + status + '\n')


def messageLen(data, client):
    length = len(pickle.dumps(data))
    client.send(pickle.dumps(length))


def getBoards(client, clientAddress, time):
    os.chdir(cwd)
    try:
        boards = os.listdir(path='board')
    except:
        print("ERROR: There is no board folder. Please create one.")
        log(clientAddress, time, "GET_BOARDS", "ERROR")
        sys.exit()

    if boards == []:
        print("ERROR: There are no boards in the board folder.")
        log(clientAddress, time, "GET_BOARDS", "ERROR")
        sys.exit()
    else:
        messageLen(boards, client)
        client.send(pickle.dumps(boards))
        print("Successfully sent list of boards.")
        log(clientAddress, time, "GET_BOARDS", "OK")


def post(boardNum, title, message, client, clientAddress, time):
    try:
        os.chdir(cwd)
        boards = os.listdir(path='board')
        title = title.replace(' ', '_')
        board = boards[int(boardNum)-1]
        boardDir = cwd + '/board'
        chosenBoardDir = boardDir + "/" + board
        os.chdir(chosenBoardDir)
        messageFile = open(time + '-' + title, "w+")
        messageFile.write(message)
        messageFile.close()
        success = "Message posted"
        messageLen(success, client)
        client.send(pickle.dumps(success))
        print("Successfully posted message.")
        log(clientAddress, time, "POST", "OK")
    except:
        print("ERROR: There was an error posting the message.")
        log(clientAddress, time, "POST", "ERROR")


def getMessages(boardNum,  client, clientAddress, time):
    os.chdir(cwd)
    boards = os.listdir(path='board')
    if boardNum.isdigit():
        if len(boards) >= int(boardNum) >= 1:
            os.chdir(cwd)
            boards = os.listdir(path='board')
            messages = []
            board = boards[int(boardNum) - 1]
            boardDir = cwd + '/board'
            chosenBoardDir = boardDir + "/" + board
            os.chdir(chosenBoardDir)
            for file in os.listdir(chosenBoardDir):
                f = open(file, "r")
                if f.mode == "r":
                    contents = f.read()
                messages.append([file, contents])
            messages.sort(reverse=True)
            messages = messages[:100]
            messageLen(messages, client)
            client.send(pickle.dumps(messages))
            print("Successfully sent recent messages.")
            log(clientAddress, time, "GET_MESSAGES", "OK")
        else:
            print("ERROR: That board does not exist.")
            log(clientAddress, time, "GET_MESSAGES", "ERROR")
    else:
        print("ERROR: A number was not supplied by the user.")
        log(clientAddress, time, "GET_MESSAGES", "ERROR")


serverName = sys.argv[1]
serverPort = sys.argv[2]
serverSocket = socket(AF_INET,SOCK_STREAM)
try:
    serverSocket.bind((serverName, int(serverPort)))
    print(f'The server is ready to recieve on {serverName}:{serverPort}...')
except:
    print('The server port is busy or doesn\'t exist.'.format(str(error)))
    sys.exit()

serverSocket.listen(1)

socketsList = [serverSocket]
clients = {}

cwd = os.getcwd()

serverSocket.setblocking(False)
logList = []

while True:

    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)

    # Iterate over notified sockets
    for currentSocket in readSockets:

        # If notified socket is a server socket - new connection, accept it
        if currentSocket == serverSocket:
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            clientSocket, clientAddress = serverSocket.accept()

            logList.append([clientAddress[0], clientAddress[1]])

            socketsList.append(clientSocket)

            print('Accepted new connection from {}:{}'.format(*clientAddress))
            now = datetime.now()
            time = now.strftime("%Y%m%d-%H%M%S")
            getBoards(clientSocket, clientAddress, time)
        else:
            try:
                pickleData = currentSocket.recv(1024)
                now = datetime.now()
                time = now.strftime("%Y%m%d-%H%M%S")
            except:
                # Remove from list for socket.socket()
                socketsList.remove(currentSocket)
                print('Disconnection from {}:{}'.format(*clientAddress))

                # Remove from our list of users

                pickleData = []

                continue
            try:
                data = pickle.loads(pickleData)
            except EOFError:
                data = []
            if data:
                instruction = data[0]
                if instruction == "GET_BOARDS":
                    getBoards(clientSocket, clientAddress, time)
                elif instruction == "POST":
                    boardNum = data[1]
                    title = data[2]
                    message = data[3]
                    if boardNum == "" or title == "" or message == "":
                        print("ERROR: There was a problem with one of the parameters.")
                        log(clientAddress, time, "POST", "ERROR")
                    else:
                        post(boardNum, title, message, clientSocket, clientAddress, time)
                elif instruction == "GET_MESSAGES":
                    getMessages(data[1], clientSocket, clientAddress, time)
                else:
                    print("ERROR: Not a defined instruction.")
                    log(clientAddress, time, "UNKNOWN", "ERROR")


