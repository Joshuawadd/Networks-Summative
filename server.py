#!/usr/bin/env python3

import os
from socket import *
from pathlib import Path
import pickle
boards = os.listdir(path='board')
#print(boards)
p = Path('./board')
print(p)
#print([x for x in p.iterdir() if x.is_dir()])
#print(os.fspath(f))
#print(p.resolve())
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    boards1 = pickle.dumps(boards)
    print(boards1)
    connectionSocket.send(boards1)
    connectionSocket.close()

def GET_BOARDS() :
    boards = os.listdir(path='board')
    print(boards[1])

def POST() :
    boardnum = input('Input the board number: ')
    title = input('Input the title: ')
    message = input('Input the message: ')

#def QUIT() :