
#taken from http://stackoverflow.com/questions/12664295/ntp-client-in-python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import datetime


global agiType
global agiStatus
global agiIndx

agiType = 0
agiIndx = 0
agiStatus = False

# accesses NTP server to get current time
# not used
def getDateTime_old():
    print "starting getDateTime()"
    host = "pool.ntp.org"
    port = 123
    buf = 1024
    address = (host,port)
    msg = '\x1b' + 47 * '\0'
    
    
    # reference time (in seconds since 1900-01-01 00:00:00)
    DST = 3600   # move time ahead 1 hour
    TIMEZONE = 4 * 3600 # EST
    TIME1970 = 2208988800L + TIMEZONE # 1970-01-01 00:00:00

    #############################
    #Modified to check 100 times#
    #############################
    for i in range(100):
    	# connect to server
    	client = socket.socket( AF_INET, SOCK_DGRAM)
    	client.settimeout(2)    

    	try:
    		client.sendto(msg, address)
    		msg, address = client.recvfrom( buf )
    	except:
        	continue
    	else:
    		t = struct.unpack( "!12I", msg )[10]
    		#print t
    		t -= TIME1970
    		#print t
    
   		print "Completed getDateTime()"
		try:
    	    		return time.ctime(t)
		except:
	    		print "Error Processing Time"
	    		continue

    print "Error Accessing NTP Server"
    return time.ctime(time.mktime(datetime.datetime.now().timetuple()))


# returns current system time on the BBB
# need to set correct time somewhere else for this to return the correct time
def getDateTime():
    return time.ctime(time.mktime(datetime.datetime.now().timetuple()))


# returns a string usable in filenames from a string representing a datetime object
# format is: year-month-day_hour-minute
def stripDateTime(dateTimeString):
	# get a list with format: [year, month, day, hour, minute, second, fraction ofa second]
	dtList =  dateTimeString.replace("-", " ").replace(":"," ").replace("."," ").split(" ")
	return dtList[0]+"-"+dtList[1]+"-"+dtList[2]+"_"+dtList[3]+"-"+dtList[4]+"-"+dtList[5]

# send an update message to the BaseStation	
global disconnFlag
disconnFlag = True
def sendUpdate(server_address, message, timeout=5):
    #iterations, message, sum1 = 0, sum2 = 0, sum3 = 0, sum4 = 0, timeout = 5):
    global disconnFlag
    global agiIndx
    global agiType
    global agiStatus

    updateSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    updateSock.settimeout(timeout)
    try:
        updateSock.connect(server_address)
        if disconnFlag:
            updateSock.sendall("Connection Up!")
            print "Connection Up!"
            disconnFlag = False
        else:
            updateSock.sendall(";".join(message))
            #updateSock.sendall("{}".format(iterations) + message + "{} {} {} {}".format(sum1,sum2,sum3,sum4))
            print "Send success for " + message[0]
            # first 3 bytes are length of message
            msgLen = ''
            while (len(msgLen) < 3):
                try:
                    msgLen = msgLen + updateSock.recv(3)
                except:
                    # if this fails, just return, which indicates failed update
                    return
            msgLen = int(msgLen)
            data = ''    
            # call recv until we get all the data
            while (len(data) < msgLen):
                try:
                    data = data + updateSock.recv(msgLen)
                except:
                    return
            splitData = data.split(";")
            agiIndx = int(splitData[0])
            agiType = int(splitData[1])
            if agiType==0:
                agiStatus = False
            else:
                agiStatus = True
            print ("Return success! {}, {}, {}".format(agiType,agiStatus,splitData[2]))
            #data format is <ShimmerID1>,<ShimmerID2>,<current time>
            # return current BS time
            return splitData[2]
            	
    except:
        print "error updating base station while in " + message[0]
        disconnFlag = True
    return

