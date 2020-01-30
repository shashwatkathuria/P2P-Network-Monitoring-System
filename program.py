# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 14:32:47 2020

@author: Shashwat Kathuria
"""

# SOCKET PROGRAMMING - PEER-TO-PEER NETWORK MONITORING SYSTEM

# Importing required libraries
import socket, threading, time

# Initializing required global varibales
ENCODING = 'utf-8'
flag = True
globalCurrentTime = None
globalReceivedTime = None
turnBoolean = True

# Inputs required
print("-----------------------------------")
myName = input("My Name : ")
myIP = "localhost"
myPort = int(input("My Port : "))


def main():
    """Main function to make threads and call sender and receiver thread."""

    # Peer information inputs
    # Inside main because there is an additional option to change to another peer after quitting
    print("-----------------------------------")
    peerName = input("Enter Peer's Name : ")
    peerIP = input("Peer's IP : ")
    peerPort = int(input("Peer's Port : "))
    print("-----------------------------------")
    print()

    # Initializing threads
    if flag == True:
        receiverThread = threading.Thread(target = listen, args = (myIP, myPort))
    senderThread = threading.Thread(target = send, args = (peerIP, peerPort))

    # Starting threads
    if flag == True:
        receiverThread.start()
    senderThread.start()

    # Joining threads
    if flag == True:
        receiverThread.join()
    senderThread.join()

def listen(myIP, myPort):
    """Funtion for Listener."""
    global globalCurrentTime, globalReceivedTime, turnBoolean

    # Establishing connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((myIP, myPort))
    sock.listen(10)

    # Always trying to connect
    while True:

        connection, client_address = sock.accept()

        # Try except for if connected or not
        try:
            receivedMessage = ""

            # Always listening once estalished
            while True:
                receivedTime = time.time()
                globalReceivedTime = receivedTime
                data = connection.recv(16)
                receivedMessage = receivedMessage + data.decode(ENCODING)

                if not data:

                    # For appropriate calculation of round trip time
                    if globalCurrentTime != None and globalReceivedTime != None:

                        # Round Trip Time (RTT) calculated and received message printed
                        print(receivedMessage.strip())
                        print("Total Round Trip Time (RTT) : " + str(globalReceivedTime - globalCurrentTime) + " seconds")

                        # Resetting variables if user again wants to calculate RTT
                        globalCurrentTime = None
                        globalReceivedTime = None
                        turnBoolean = True

                        print("\n")

                    break
        # Finally closing connection
        finally:
            connection.shutdown(2)
            connection.close()


def send(friend_IP, friend_port):
    """Funtion for Sender."""
    global globalCurrentTime, globalReceivedTime, turnBoolean

    # Always running until user quits
    while True:

        # Extra variable to break from the outer loop
        breakOuter = False

        # Due to turn wise calculation for round trip
        while turnBoolean:

            # Option to quit or send message
            option = input("Y or y to send message, N or n to quit : ")

            # Quitting if n or N
            if option == "n" or option == "N":
                global flag
                flag = False
                breakOuter = True
                break

            # Establishing connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Getting the status of receiver
            result = s.connect_ex((friend_IP, friend_port))

            # Printing status and sending timestamp if online
            if result == 0:
                print("Status : Your peer is ONline.")

                # Sending message
                currentTime = time.time()
                messageWithTimeStamp = "Time Stamp : " + myName + " : " + str(currentTime)
                globalCurrentTime = currentTime

                s.sendall(messageWithTimeStamp.encode(ENCODING))

                # Turn to wait for response now
                turnBoolean = False
                s.shutdown(2)
                print("Waiting for the response to finish....")

            # Printing status and terminating if offline
            else:
                print("Status : Your peer is OFFline.")
            s.close()

        # To break from the outer loop
        if breakOuter == True :
            break

    # To connect to another peer after quitting connnection
    main()

# Calling main function
if __name__ == "__main__":
    main()
