from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from threading import Thread

#Functionality for handling new connections
def accept_new_connections():
    while True:
        #socket.accept() returns a socket object, and the associated address
        client, client_address = SERVER.accept()
        print ("%s:%s has connected to the server." % client_address)
        #converts a string to a utf8 encoded bytearray object and sends it to the client socket
        client.send(bytes("Enter name: ", "utf8"))
        #Stores new client address in a dictionary indexed by the associated socket
        addresses[client] = client_address
        #Creates a thread to handle new client making the server asynchronous
        Thread(target=client_interaction, args=(client,)).start()

#Functionality for handling client interaction. (argument == client socket)
def client_interaction(client):
    name = client.recv(BUFFER_SIZE).decode("utf8")
    welcome = "Welcome %s, to quit enter '~quit'" % name
    client.send (bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast (bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg != bytes ("~quit", "utf8"):
            broadcast (msg, name+": ")
        else:
            client.send(bytes("~quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s exited the chat." % name, "utf8"))
            break

#Functionality to communicate with all connected clients.
def broadcast(message, name=""):
    for sockets in clients:
        sockets.send(bytes(name, "utf8") + message)

clients = {}
addresses = {}

#Constants used by server
HOST = ''
PORT = 33000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
MAX_CLIENTS = 16

#Creates a socket for the server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_new_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
