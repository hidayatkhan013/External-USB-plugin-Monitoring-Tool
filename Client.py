import socket
import socket
import getpass
import subprocess
from time import sleep
import pickle
import psutil
import os

def establishConnection():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("192.168.100.8",9090))
        return clientSocket
    except socket.error as e:
        print(str(e))

    

def getHostIp():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.connect(("8.8.8.8", 80))
    return conn.getsockname()[0]

def getMacAdress(ip_host):
    nics = psutil.net_if_addrs()
    for i in nics:
        if ip_host in nics[i][1]:
            return nics[i][0].address

def getUserName():
    return getpass.getuser()

def getHostName():
    return socket.gethostname()

def getWorkgroup():
    return subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"], stdout=subprocess.PIPE, text=True).stdout.strip()


if __name__ == "__main__":
    connectClient=establishConnection()
    while True:
        username=getUserName()
        hostname = getHostName()
        workgroup = getWorkgroup()
        ip_host=getHostIp()
        mac= getMacAdress(ip_host)
        # print("Host name : ",hostname)
        # print("User name : ",username)
        # print("Ip : ",ip_host)
        # print("MAC : ",mac)
        # print("Domain : ",workgroup)
        lst=[hostname,username,ip_host,mac,workgroup]
        data1=pickle.dumps(lst)
        connectClient.send(data1)
        dataFromServer = connectClient.recv(1024)
        CommandFromServer = dataFromServer.decode()
        print(CommandFromServer)
        if CommandFromServer.lower()=="logout":
            print("loggingout down in 3 seconds")
            sleep(3)
            os.system("shutdown /l")
        sleep(10)

    connectClient.close()

