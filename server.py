#!/usr/bin/env python3


from socket import *
import select
import sys
import os
import pickle
from datetime import datetime


def messageLen(data, client):
    length = len(pickle.dumps(data))
    client.send(pickle.dumps(length))


def getBoards(client):
    os.chdir(cwd)
    boards = os.listdir(path='board')
    print("sending")
    messageLen(boards, client)
    client.send(pickle.dumps(boards))


def post(boardNum, title, message, client) :
    os.chdir(cwd)
    boards = os.listdir(path='board')
    title = title.replace(' ', '_')
    now = datetime.now()
    time = now.strftime("%Y%m%d-%H%M%S")
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
    print("Successful")


def getMessages(boardNum,  client):
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
    messages = messages[-100:]
    messageLen(messages, client)
    client.send(pickle.dumps(messages))
    print("Successful")



serverName = sys.argv[1]
serverPort = int(sys.argv[2])
serverSocket = socket(AF_INET,SOCK_STREAM)
try:
    serverSocket.bind((serverName, serverPort))
    print(f'The server is ready to recieve on {serverName}:{serverPort}...')

except IOError as error:
    print('The server port is busy or doesn\'t exist.'.format(str(error)))
    sys.exit()
serverSocket.listen(1)

socketsList = [serverSocket]
clients = {}

cwd = os.getcwd()

serverSocket.setblocking(False)

while True:

    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)

    # Iterate over notified sockets
    for currentSocket in readSockets:

        # If notified socket is a server socket - new connection, accept it
        if currentSocket == serverSocket:
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            clientSocket, clientAddress = serverSocket.accept()

            socketsList.append(clientSocket)

            print('Accepted new connection from {}:{}'.format(*clientAddress))
            getBoards(clientSocket)
        else:
            try:
                pickleData = currentSocket.recv(1024)
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
                    getBoards(clientSocket)
                elif instruction == "POST":
                    boardNum = data[1]
                    title = data[2]
                    message = data[3]
                    post(boardNum, title, message, clientSocket)
                elif instruction == "GET_MESSAGES":
                    getMessages(data[1], clientSocket)


