import socket
import sys,os
import pickle
from database import *


# creating socket
def createSocket():
    try:
        soc=socket.socket()
        return soc
    except socket.error as msg:
        print(msg)

# bing the socket
def bindSocket(socket):
    try:
        print(f"Binding the Port : {port}")
        socket.bind((host,port))
        print("listening......")
        socket.listen(2)
    except socket.error as msg:
        print(msg)
        print("Retrying.........")
        bindSocket(socket)

# accpting connection
def acceptConn(socket):
    while True:
        conn,adrss=socket.accept()
        print(f"Connected to : {adrss[0]} : {adrss[1]}")
        responce=conn.recv(1024)
        data=pickle.loads(responce)
        print(data)
        main_db(data)







if __name__ == "__main__":
    host="192.168.100.8"
    port=9090
    socket=createSocket()
    bindSocket(socket)
    acceptConn(socket)
    
    os.system("pause")
    