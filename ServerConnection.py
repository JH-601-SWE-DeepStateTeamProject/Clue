#!/usr/bin/python3

import socket
import sys
import _thread
import queue
from array import array
import time

# memory allocation
dataFromClient = queue.Queue()
dataToSendClient = queue.Queue()

# network configuration

serverAddress = ('localhost', 4211)
clientAddress = ('localhost', 4212)

ProtocolID = 0x7A28


def send_data_to_client():
    print("1")
    while True:
        data_item = dataToSendClient.get()
        #clientConnection.sendto(data_item, clientAddress)
        print("Sent data to client...")


def receive_data_from_client():
    print("2")
    client_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_connection.bind(serverAddress)
    while True:
        data_item, address = client_connection.recvfrom(2048)
        dataFromClient.put(data_item)
        print("Received data from client...")


def verify_client_data():
    print("3")
    while True:
        data_item = dataFromClient.get()
        if data_item[1] == 0x7A and data_item[0] == 0x28:
            print("valid data")
        else:
            print("INVALID data")


def main():
    print(sys.version)
    print("Starting up server...")
    _thread.start_new_thread(send_data_to_client, ())
    _thread.start_new_thread(receive_data_from_client, ())
    _thread.start_new_thread(verify_client_data, ())

    # keep main thread running for subthreads to not exit
    while 1:
        pass


main()
