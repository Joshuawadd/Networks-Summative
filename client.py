#!/usr/bin/env python3

import sys
from socket import *
import pickle


def getBoards():
    instruction = ["GET_BOARDS"]
    clientSocket.send(pickle.dumps(instruction))
    length = pickle.loads(clientSocket.recv(10))
    pickleBoardList = clientSocket.recv(length)
    boardList = pickle.loads(pickleBoardList)
    a = 1
    print("From server: ")
    for i in boardList:
        print(a, ': ', i)
        a = a + 1
    return boardList


def post():
    information = []
    instruction = "POST"
    information.append(instruction)
    numSelection = True
    while numSelection:
        boardNum = input('Input the board number: ')
        try:
            if len(boardList) >= int(boardNum) >= 1:
                numSelection = False
                print("Not a valid board selection.")
            else:
                numSelection = True
                print("Not a valid board selection.")
        except:
            numSelection = True
            print("Please enter a number for the board selection.")
    information.append(boardNum)
    title = input('Input the title: ')
    information.append(title)
    message = input('Input the message: ')
    information.append(message)
    clientSocket.send(pickle.dumps(information))
    length = pickle.loads(clientSocket.recv(10))
    print(pickle.loads(clientSocket.recv(length)))


def getMessages(boardNum):
    information = ["GET_MESSAGES", boardNum]
    clientSocket.send(pickle.dumps(information))
    length = pickle.loads(clientSocket.recv(10))
    print(length)
    messageList = pickle.loads(clientSocket.recv(length))
    if messageList == []:
        print("There are no messages on this board")
    else:
        print("Most recent messages from this board: ")
        print()
        for i in reversed(messageList):
            print(i[0] , " : ", '"', i[1], '"')
    print()

def quit():
    clientSocket.close()
    sys.exit()


serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
length = pickle.loads(clientSocket.recv(10))
pickleBoardList = clientSocket.recv(length)
boardList = pickle.loads(pickleBoardList)
print(boardList)
a = 1
print("From server: ")
for i in boardList:
    print(a, ': ', i)
    a = a + 1
print("Please enter one of the following commands:")
print()
print("POST - to post a message to one of the boards,")
print("GET_BOARDS - to view again the list of available boards,")
print("Or the number of the board you would like to see the most recent messages from.")
print()
while True:
    command = input('Input a command:')
    if command == "POST":
        post()
    elif command == "GET_BOARDS":
        getBoards()
    elif command == "QUIT":
        quit()
    elif command.isdigit():
        if len(boardList) >= int(command) >= 1:
            getMessages(command)



