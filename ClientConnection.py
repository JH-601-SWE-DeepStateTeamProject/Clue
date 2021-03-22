#!/usr/bin/python3

import socket
import sys
import _thread
import queue
from array import array
import time

dataFromServer = queue.Queue()
dataToSendServer = queue.Queue()
serverConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 4211)
ProtocolID = 0x7A28
payload = b"cluelessdata"
sourceID = 1
destID = 10
ServerID = 50
    
def SendDataToServer():
    while True:
        dataItem = dataToSendServer.get()
        serverConnection.sendto(dataItem, server_address)
        print("Sent data to server...")

def ReceiveDataFromServer():
    while True:
        dataItem = serverConnection.recvfrom(2048)
        dataFromServer.push(dataItem)

def CalculateChecksum(binaryData):
    checksum = 0
    checksum = sum(binaryData)
    binaryData.extend((checksum//256, checksum % 256))
    return binaryData

def main():
    print(sys.version)
    print("Starting up client...")
    _thread.start_new_thread(SendDataToServer, ())
    _thread.start_new_thread(ReceiveDataFromServer, ())

    for count in range(3):
        byteData = bytearray()
        byteData.extend(ProtocolID.to_bytes(2, 'little'))
        byteData.extend(len(payload).to_bytes(2, 'little'))
        byteData.extend(sourceID.to_bytes(2, 'little'))
        byteData.extend(destID.to_bytes(2, 'little'))
        byteData.extend(ServerID.to_bytes(2, 'little'))
        byteData = CalculateChecksum(byteData)
        byteData.extend(payload)
        dataToSendServer.put(byteData)
        time.sleep(1)

    invalid_byte_data = bytearray()
    invalid_byte_data.extend(ProtocolID.to_bytes(2, 'big'))
    dataToSendServer.put(invalid_byte_data)
    time.sleep(1)

main()