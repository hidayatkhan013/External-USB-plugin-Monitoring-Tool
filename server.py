import socket
import sys,os
import pickle
from database import *
from _thread import *


ThreadCount = 0
def multi_threaded_client(connection,hostaddrs):
    while True:
        try:
            connection.sendall(str.encode('Server is Up:')) 
        except Exception as msg:
            print(msg)
        try:
            responce=connection.recv(1024)
        except Exception as msg:
            print("client is disconnect : ",hostaddrs)
            break;
        data=pickle.loads(responce)
        print(data)
        main_db(data)

        # connection.sendall(str.encode(response))
    connection.close()


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
        socket.listen(10)
    except socket.error as msg:
        print(msg)
        print("Retrying.........")
        bindSocket(socket)

# accpting connection
def acceptConn(socket):
    while True:
        conn,adrss=socket.accept()
        print(f"Connected to : {adrss[0]} : {adrss[1]}")
        start_new_thread(multi_threaded_client, (conn,adrss, ))
        global ThreadCount
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

    socket.close()




if __name__ == "__main__":
    host="192.168.100.8"
    port=9090
    socket=createSocket()
    bindSocket(socket)
    acceptConn(socket)
    os.system("pause")
    