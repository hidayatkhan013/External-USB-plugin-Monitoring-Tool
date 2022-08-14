from http import client
import socket
import socket
import getpass
import subprocess
from time import sleep
import pickle
import psutil
import os
from DetectUSB import *
from _thread import *
import os,string,time
from ctypes import windll
from Client import *





class Client:
    def __init__(self):
        self.connectClient = self.establishConnection()

    def establishConnection(self):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(("192.168.100.8",9090))
            return clientSocket
        except socket.error as e:
            print("Server is Down")
    def getHostIp(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn.connect(("8.8.8.8", 80))
        return conn.getsockname()[0]
    def getMacAdress(self , ip_host):
        nics = psutil.net_if_addrs()
        for i in nics:
            if ip_host in nics[i][1]:
                return nics[i][0].address

    def getUserName(self):
        return getpass.getuser()

    def getHostName(self):
        return socket.gethostname()

    def getWorkgroup(self):
        return subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"], 
        stdout=subprocess.PIPE, text=True).stdout.strip()

    def get_driveStatus(self):
        devices = []
        record_deviceBit = windll.kernel32.GetLogicalDrives()#The GetLogicalDrives function retrieves a bitmask
                                                            #representing the currently available disk drives.
        for label in string.ascii_uppercase : #The uppercase letters 'A-Z'
            if record_deviceBit & 1:
                devices.append(label)
            record_deviceBit >>= 1
        return devices

    def detect_device(self):
            original = set(self.get_driveStatus())
            print ('Detecting...')
            time.sleep(3)
            add_device =  set(self.get_driveStatus())- original
            subt_device = original - set(self.get_driveStatus())
            if (len(add_device)):
                # print ("There were %d"% (len(add_device)))
                # for drive in add_device:
                #         print ("The drives added: %s." % (drive))
                return 1
            elif(len(subt_device)):
                # print ("There were %d"% (len(subt_device)))
                # for drive in subt_device:
                #         print ("The drives remove: %s." % (drive))
                return -1

    def DetectUSBmain(self):
        while True:
            detect = self.detect_device()
            username = self.getUserName()
            hostname = self.getHostName()
            workgroup = self.getWorkgroup()
            self.ip_host = self.getHostIp()
            mac = self.getMacAdress(self.ip_host)
            if detect==1:
                print("USB device is plugin to PC :\n")
                data1=pickle.dumps(("USB device is plugin to PC IP : "+str(self.ip_host)))
                self.connectClient.send(data1)
                lst=[hostname,username,self.ip_host,mac,workgroup]
                data1=pickle.dumps(lst)
                self.connectClient.send(data1)
            elif detect==-1:
                print("USB device is plugout to PC :\n")
                data1=pickle.dumps(("USB device is plugout to PC IP : "+str(self.ip_host)))
                self.connectClient.send(data1)
                lst=[hostname,username,self.ip_host,mac,workgroup]
                data1=pickle.dumps(lst)
                self.connectClient.send(data1)
            else:
                data1=pickle.dumps(("Client is UP : "+str(self.ip_host)))
                self.connectClient.send(data1)


if __name__ == "__main__":
    obj = Client()
    detect= start_new_thread(obj.DetectUSBmain, ())
    while True:
        try:
            dataFromServer = obj.connectClient.recv(1024)
            CommandFromServer = dataFromServer.decode()
            print(CommandFromServer)
            if CommandFromServer.lower()=="logout":
                print("loggingout down in 3 seconds")
                sleep(3)
                os.system("shutdown /l")
        except Exception as e:
            print("Server is not responding")
            break
        sleep(3)
    try:
        obj.connectClient.close()
    except Exception as e:
        print("server is not running")
