import socket
import sys,os
import pickle
from database import *
from _thread import *

import logging
import logging.handlers
import os
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "yourapp.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)



logging.info('Start of Log')


ThreadCount = 0
def multi_threaded_client(connection,hostaddrs):
    while True:
        try:
            # if hostaddrs[0]=='192.168.100.6':
            #     userCommand=input("enter command : ")
            #     connection.send(str.encode(userCommand))
            connection.sendall(str.encode('Server is Up:')) 
        except Exception as msg:
            logging.exception(msg)
        try:
            responce=connection.recv(1024)
        except Exception as msg:
            logging.exception("client is disconnect : ",hostaddrs)
            break;
        data=pickle.loads(responce)
        # print(data)
        logging.info(data)
        if len(data)>50:
            main_db(data)

        # connection.sendall(str.encode(response))
    connection.close()


# creating socket
def createSocket():
    try:
        soc=socket.socket()
        return soc
    except socket.error as msg:
        logging.warning(msg)

# bing the socket
def bindSocket(socket):
    try:
        print(f"Binding the Port : {port}")
        socket.bind((host,port))
        print("listening......")
        socket.listen(10)
    except socket.error as msg:
        logging.exception(msg)
        print(msg)
        print("Retrying.........")
        bindSocket(socket)

# accpting connection
def acceptConn(socket):
    while True:
        conn,adrss=socket.accept()
        print(f"Connected to : {adrss[0]} : {adrss[1]}")
        logging.warning(f"Connected to : {adrss[0]} : {adrss[1]}")
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
    