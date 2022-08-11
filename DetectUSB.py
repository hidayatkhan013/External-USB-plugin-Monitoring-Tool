import os,string,time
from ctypes import windll
from Client import *

def get_driveStatus():
    devices = []
    record_deviceBit = windll.kernel32.GetLogicalDrives()#The GetLogicalDrives function retrieves a bitmask
                                                         #representing the currently available disk drives.
    for label in string.ascii_uppercase : #The uppercase letters 'A-Z'
        if record_deviceBit & 1:
            devices.append(label)
        record_deviceBit >>= 1
    return devices

def detect_device():
        original = set(get_driveStatus())
        print ('Detecting...')
        time.sleep(3)
        add_device =  set(get_driveStatus())- original
        subt_device = original - set(get_driveStatus())
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

def DetectUSBmain(connectClient):
    while True:
        detect = detect_device()
        username = getUserName()
        hostname = getHostName()
        workgroup = getWorkgroup()
        ip_host=getHostIp()
        mac= getMacAdress(ip_host)
        if detect==1:
            print("USB device is plugin to PC :\n")
            data1=pickle.dumps(("USB device is plugin to PC IP : "+str(ip_host)))
            connectClient.send(data1)
            lst=[hostname,username,ip_host,mac,workgroup]
            data1=pickle.dumps(lst)
            connectClient.send(data1)
        elif detect==-1:
            print("USB device is plugout to PC :\n")
            data1=pickle.dumps(("USB device is plugout to PC IP : "+str(ip_host)))
            connectClient.send(data1)
            lst=[hostname,username,ip_host,mac,workgroup]
            data1=pickle.dumps(lst)
            connectClient.send(data1)
        else:
            data1=pickle.dumps(("Client is UP : "+str(ip_host)))
            connectClient.send(data1)

