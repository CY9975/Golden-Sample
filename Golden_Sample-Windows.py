# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import serial
import time
import json
import requests

STREAMID=input('Enter DEVICE ID from M2X:')
apikey=input('Enter API KEY from M2X:')
dev0ID=STREAMID
h1={'X-M2X-KEY': '%s' % (apikey)}
h2={'X-M2X-KEY': '%s' % (apikey), 'Content-Type': 'application/json'}
url='http://api-m2x.att.com/v2/devices/'
jsonp='?pretty=true'
#Insert series ot AT Commands to be exexute executed.
AT_COMMANDS=["AT+CSQ\r","AT+CREG=2\r","AT+CREG?\r","ATI\r","AT+ICCID\r"]
#Stored AT responses
AT_RESPONSES=[]



def postm2x(stream,val):      #establish a loop to attempt to POST data
    data1={'value':val }
    
    try:
        response = requests.put(url+dev0ID+action+jsonp, data=json.dumps(data1), headers=h2)
	
        if (response.status_code) == 202:
            print (response.status_code)
            print ('Posted new value=', val ,'to stream.   Accepted.\n')
        else:
            print ('Response not 202...Error!!!  \n')
            print ('response.text gives:\n')
            print (response.text)
    except:      #Error handling, such as wifi connection dropped
        print ('post Exception raised: ')
        time.sleep(20)    #give connection some time to reconnect


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

    ser.close()#Closes serial port.

#Splice device info from list and strip unwanted info.
dev=AT_RESPONSES[3]
dev=dev.replace("ATI","")
dev=dev.replace("OK","")
dev=dev.replace("+GCAP: +CGSM,+DS,+ES","")
dev=dev.replace("SVN: 01","")
#print(dev)

#Splice ICCID info from list and strip unwanted info.
ICCID=AT_RESPONSES[4]
ICCID=ICCID.replace("AT+ICCID","")
ICCID=ICCID.replace("OK","")
#print(ICCID)

#Splice signal quality from list and strip unwanted info.
csq=AT_RESPONSES[0]
csq=csq.strip("\r")
csq=csq.strip("AT+CSQ")
csq=csq.replace("OK","")
csq=csq.replace("+CSQ:","")
csq=csq.replace(",99","")
csq=int(csq) 

if (csq >=0) and (csq <=9):
    signal=('Signal stregnth is Marginal.   ')
elif(csq >=10) and (csq <=14):
    signal=("Signal stregnth is OK.   ")
elif(csq>=15) and (csq<=19):
    signal=("Signal stregnth is Good.   ")
elif (csq>20):
    signal=("Signal stregnth is Excellent.   " )
else:
    print("ERROR")
print(signal)  
#Splice regisration info from list and strip unwanted info.
CREGr=AT_RESPONSES[2]
CREGr=CREGr.strip("AT+CREG?")
CREGr=CREGr.replace("OK","")
CREGr=CREGr.replace("\r","")
CREGr=CREGr.strip("\n")
CREGr=CREGr.replace("OK","")
CREGr=CREGr.replace('"',"")
CREGr=CREGr.replace("+CREG:","")
CREGr=CREGr.replace(" ","")
res=CREGr.split(",")#Split regisration info
#Resisration Status.
regstat=int((res[1]))
#Local area code.
loc_area_code=(res[2])
#Cellis
cellid=(res[3])
#Access Technology
acctech=int((res[4]))
#Regisration status if
if regstat==0:
    reg=("Registration status:not registered; MT is not currently searching a new operator" 
        "to register to.   ")
    print (reg)
elif regstat==1:
    reg=("Registration status:registered, home network.   ")
    print(reg)
elif regstat==2:
    reg=("Registration status:not registered; but MT is currently searching a new operator to" 
    "register to.   ")
    print (reg)
elif regstat==3:
    reg=("Registration status:registration denied.   ")
    print (reg)
elif regstat==4:
    reg=("Registration status:unknown.   ")
    print (reg)
elif regstat==5:
    reg=("Registration status:registered, roaming.   ")
    print (reg)
else:
    print("ERROR")

#Access tech if
if acctech==0:
    tech=("GSM   ")
elif acctech==1:
    tech=("GSM Compact   ")
elif acctech==2:
    tech=("UTRAN   ")
elif acctech==3:
    tech=("GSM w/EGPRS   ")
elif acctech==4:
    tech=("UTRAN w/HSDPA   ")
elif acctech==5:
    tech=("UTRAN w/HSDPA   ")
elif acctech==6:
    tech=("UTRAN w/HSDPA and HSUPA   ")
elif acctech==7:
    tech=("E-UTRAN   ")
else:
    print("ERROR SITE")

#print("Access Technology:",tech,".")


#Converts local areacode from Hex to int.
loc_area_code = int(loc_area_code, 16) #Hex to str.
areacode= "The local area code is",loc_area_code,"."
#print(areacode)

#
#ser.close()#Making sure serial is closed(not nessesary)


z=0
while z==0:
    connec=input("Open Connection Manager,press Y when complete.")
    if connec=="Y":
         print("Test running....")
         test=os.popen("speedtest-cli").read()
         #print(test)
         break
         
    else:
        print("INVALID RESPONSE SELF DESTRUCT SEQUENCE ACTIVATED")
        for i in[10,9,8,7,6,5,4,3,2,1]:
                print (i)
                time.sleep(1)
                z=0
#Stream dictionary.
streamvalue={"Device_Info":dev ,"ICCID":ICCID,"Signal":csq,"RegStat":regstat,"AccessTech":acctech,"Local_Code":loc_area_code,"cellid":cellid,"Stream":test}
#Name of streams/
streams=["Device_Info","ICCID","Signal","RegStat","AccessTech","Local_Code","cellid","Stream"]
#Changes the action to post to individual streams.
for b in streams:
    action='/streams/%s/value' % (b)  # Action for updating a stream with data
    postm2x(b,streamvalue[b])

print("Complete!")

    
