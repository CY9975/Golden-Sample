# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 07:23:39 2016

@author: E_W7
"""

import serial
import time

AT_COMMANDS=["AT$QCRSRP?\r"]
#Stored AT responses
AT_RESPONSES=[]

#Prompt user for device com port.
COM=input('Enter COM Port Name Ex"COM11":')
for i in AT_COMMANDS:
    msg = (i).encode()#Convert str to bytes
    ser = serial.Serial(COM, 9600, timeout=1)#Establish com port
    ser.write(msg)#Write AT command to serial port
    time.sleep(.02)#Delay that allows HDK to process AT commands.
    r = ser.read(1024)#Read responses.
    r=r.decode()#Convert bytes to str.
    AT_RESPONSES.append(r)#Store responses to list.
    print(AT_RESPONSES)
    ser.close()#Closes serial port.
    
print(AT_COMMANDS)