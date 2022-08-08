import socket
import socket
import getpass
import subprocess
import re, uuid,os
import pickle
import psutil

def establishConnection():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("192.168.100.8",9090))
    return clientSocket

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

connectClient=establishConnection()

username=getUserName()
hostname = getHostName()
workgroup = getWorkgroup()
ip_host=getHostIp()
mac= getMacAdress(ip_host)

print("Host name : ",hostname)
print("User name : ",username)
print("Ip : ",ip_host)
print("MAC : ",mac)
print("Domain : ",workgroup)





# while True:
    # data = input("Say to server : ")
lst=[hostname,username,ip_host,mac,workgroup]
data1=pickle.dumps(lst)
connectClient.send(data1)
dataFromServer = connectClient.recv(1024)
print(dataFromServer.decode())
os.system("pause")

    # if data=='1':
    #     clientSocket.close