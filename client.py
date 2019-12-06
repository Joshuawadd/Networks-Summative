#!/usr/bin/env python3

import sys
from socket import *
import pickle


def getBoards():
    instruction = ["GET_BOARDS"]
    clientSocket.send(pickle.dumps(instruction))
    try:
        pickleBoardList = clientSocket.recv(1024)
        boardList = pickle.loads(pickleBoardList)
    except:
        print("ERROR: There was an error getting the boards from the server.")
        quit()
    a = 1
    print("From server: ")
    for i in boardList:
        boardName = i.replace('_', ' ')
        print(a, ': ', boardName)
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
    try:
        print(pickle.loads(clientSocket.recv(1024)))
    except:
        print("ERROR: There was an error posting the message")


def getMessages(boardNum):
    information = ["GET_MESSAGES", boardNum]
    clientSocket.send(pickle.dumps(information))
    try:
        messageList = pickle.loads(clientSocket.recv(1024))
    except:
        print("ERROR: There was an error getting the recent messages.")
        return
    if messageList == []:
        print("There are no messages on this board")
    else:
        print("Most recent messages from this board: ")
        print()
        for i in messageList:
            i[0] =i[0].replace('_', ' ')
            print(i[0] , " : ", '"', i[1], '"')
    print()

def quit():
    clientSocket.close()
    sys.exit()


serverName = sys.argv[1]
serverPort = sys.argv[2]
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverName, int(serverPort)))
except:
    print("The server is  not running/unavailable.")
    quit()
clientSocket.settimeout(10)
try:
    pickleBoardList = clientSocket.recv(1024)
    boardList = pickle.loads(pickleBoardList)
except:
    print("There was an error getting the boards from the server.")
    quit()
a = 1
print("From server: ")
for i in boardList:
    boardName = i.replace('_', ' ')
    print(a, ': ', boardName)
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
        else:
            print("ERROR: Please enter the number of an available board.")
            clientSocket.send(pickle.dumps(command))

    else:
        print("ERROR: Please enter a correct command.")
        print()
        clientSocket.send(pickle.dumps(command))



