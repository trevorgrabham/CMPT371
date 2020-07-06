from socket import *
import random
import sys
import time

timeSeed = int(input('Enter value to seed the time random number generator: '))
numSegs = int(input('Enter the number of segments that are to be sent: '))
ackSeed = int(input('Enter the value to seed the random number generator for a corrupted ACK: '))
prob = float(input('Enter the proability that the ACK has been corrupted: '))
dataSeed = int(input('Enter the value to seed the random number generator for the data: '))
rtt = float(input('Enter the value of the round trip time: '))
dataGen = random.Random()
dataGen.seed(dataSeed)
timeGen = random.Random()
timeGen.seed(timeSeed)
ackGen = random.Random()
ackGen.seed(ackSeed)
serverName = "127.0.0.1"
serverPort = 50007
clientSocket = socket(AF_INET,SOCK_DGRAM)
startTime = time.time()
sendTime = timeGen.random() * 5
i = 0
while i < numSegs:
    if (time.time() - startTime) < sendTime:
        continue
    seqSeg = i%2
    print('A data segment with sequence number',seqSeg,'is about to be sent')
    data = int(dataGen.random() * 1024)
    seqAck = 0
    isack = 0
    timeoutTime = rtt
    while (time.time() - timeoutTime) >= rtt:
        try:
            print('Segment sent: data =',data,'seqSeg=',seqSeg,'seqAck = 0 isack = 0')
            print('The sender is moving to state WAIT FOR ACK',seqSeg)
            segment = (data,seqSeg,seqAck,isack)
            segment = str(segment)[1:-1]
            clientSocket.sendto(segment.encode(),(serverName,serverPort))
            timeoutTime = time.time()
            clientSocket.settimeout(rtt)             
            responseSeg, serverAddress = clientSocket.recvfrom(2048)
            clientSocket.settimeout(None)  
        except:
            pass
    corrupt = ackGen.random() < prob
    while corrupt:
        print('A Corrupted ACK segment has just been received')
        print('The sender is moving back to state WAIT FOR ACK',seqSeg)
        print('A data segment with sequence number',seqSeg,'is about to be resent')
        corrupt = ackSeed.random() < prob
    recvData, recvSeqSeg, recvSeqAck, recvIsack = responseSeg.decode().replace(' ','').split(',')
    if recvSeqAck == 1:
        print('An ACK1 segment has just been received')
    else:
        print('An ACK0 segment has just been received')
    print('ACK received: data =',recvData,'seqSeg =',recvSeqSeg,'seqAck =',recvSeqAck,'isAck = 1')
    print('The sender is moving to state WAIT FOR CALL',(seqSeg+1)%2,'FROM ABOVE') 
    i += 1
    sendTime += (timeGen.random()*5)
    
clientSocket.close()

