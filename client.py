#!/usr/bin/env python3

import sys
from socket import *
import pickle
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
boardlist = clientSocket.recv(1024)
a=1
for i in pickle.loads(boardlist):
    print('From Server: ', a, ': ', i)
    a=a+1
clientSocket.close()
command = input('Input a command:')
if command == "POST":
    POST()
elif command == "QUIT":
    QUIT()


def GET_BOARDS() :
    boards = os.listdir(path='board')
    print(boards[1])


def POST() :
    boardnum = input('Input the board number: ')
    title = input('Input the title: ')
    message = input('Input the message: ')


def QUIT(a) :
    clientSocket.close()