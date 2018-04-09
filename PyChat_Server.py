from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from threading import Thread

#Constants used by server
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
#Creates a socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#Functionality for handling new connections
def accept_new_connections:
    while True:
        #socket.accept() returns a socket object, and the associated address
        client, client_address = SERVER.accept()
        print ("%s:%s has connected to the server." % client_address)
        client.send(bytes("Enter name: ", "utf8"))
        #Stores new client address in a dictionary indexed by the associated socket
        addresses[client] = client_address
        #Creates a thread to handle new client making the server asynchronous
        Thread(target=handle_client, args=(client,)).start()
