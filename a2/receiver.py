from socket import *
import random
import sys

seed = sys.argv[1]
prob = sys.argv[2]
randomGen = Random()
randomGen.seed(seed)
serverHost = '127.0.0.1'
serverPort = 50007
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((serverHost,serverPort))
print('The server is ready to recieve')
expected = 0
while True:
    segment, clientAddress = serverSocket.recvfrom(1024)
    randomNum = randomGen.random()
    if randomNum < prob:
        print('A Corrupted segment has been received')
        corrupt = 1
        print('The receiver is moving back to state WAIT FOR' + expected + 'FROM BELOW')
    else:
        corrupt = 0
        data, seqSeg, seqAck, isack = segment.decode()
        if expected == seqSeg:
            print('A segment with sequence number' + seqSeg + 'has been received')
            print('Segment received contains: data' + data + 'seqSeg=' + seqSeg + 'seqAck=' + seqAck + 'isack=' isack)
            if expected == 1:
                print('An ACK1 is about to be sent')
                ACK = (0,expected,1,1)
                print('ACK to send contains: data = 0 seqSeg = 0 seqAck = 1 isack = 1')
                expected = 0
            else:
                print('An ACK0 is about to be sent')
                ACK = (0,expected,0,1)
                print('ACK to send contains: data = 0 seqSeg = 1 seqAck = 0 isack = 1')
                expected = 1
            print('The receiver is moving to state WAIT FOR' + expected + 'FROM BELOW')
            serverSocket.sendto(ACK.encode(),clientAddress)
        else:
            print('A duplicate segment with sequence number' + seqSeg + 'has been received')
            print('Segment received contains: data' + data + 'seqSeg=' + seqSeg + 'seqAck=' + seqAck + 'isack=' isack)
    