from socket import *
import random
import sys

timeSeed = sys.argv[1]
numSegs = sys.argv[2]
ackSeed = sys.argv[3]
prob = sys.argv[4]
dataSeed = sys.argv[5]
rtt = sys.argv[6]
dataGen = Random()
dataGen.seed(dataSeed)
timeGen = Random()
timeGen.seed(timeSeed)
ackGen = Random()
ackGen.seed(ackSeed)
serverName = "127.0.0.1"
serverPort = 50007
clientSocket = socket(AF_INET,SOCK_DGRAM)

for i in range(numSegs):
    seqSeg = i%2
    print('A data segment with sequence number' + seqSeg + 'is about to be sent')
    data = int(dataGen.random() * 1024)
    seqAck = 0
    isack = 0
    print('Segment sent: data =' + data +  'seqSeg=' + seqSeg +  'seqAck = 0 isack = 0')
    print('The sender is moving to state WAIT FOR ACK' + seqSeg)
    segment = (data,seqSeg,seqAck,isack)
    clientSocket.sendto(segment.encode(),(serverName,serverPort))
    responseSeg, serverAddress = clientSocket.recvfrom(2048)
    corrupt = ackSeed.random() < prob
    while corrupt:
        print('A Corrupted ACK segment has just been received')
        print('The sender is moving back to state WAIT FOR ACK' + seqSeg)
        print('A data segment with sequence number' + seqSeg + 'is about to be resent')
        corrupt = ackSeed.random() < prob
    recvData, recvSeqSeg, recvSeqAck, recvIsack = responseSeg.decode()
    if recvSeqAck == 1:
        print('An ACK1 segment has just been received')
    else:
        print('An ACK0 segment has just been received')
    print('ACK received: data =' + recvData + 'seqSeg =' + recvSeqSeg + 'seqAck =' + recvSeqAck + 'isAck = 1')
    print('The sender is moving to state WAIT FOR CALL' + (seqSeg+1)%2 + 'FROM ABOVE') 
    
clientSocket.close()

# no idea what to do about timing...