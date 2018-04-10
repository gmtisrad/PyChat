from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from threading import Thread
import tkinter as tk

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def receive():
    while True:
        msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
        msg_queue.insert(tkinter.END, msg)

def send(event = None):
    msg = my_msg.get()
    my_msg.set("Enter Text...")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "~quit":
        client_socket.close()
        top.quit()

#Closes socket and gui window
def gui_close(event = None):
    my_msg.set("~quit")
    send()

top = tk.Tk()
top.title("PyChat")
chat_frame = tk.Frame(top)
#tkinter string type
my_msg = tk.StringVar()
my_msg.set("Enter Text...")
scrollbar = tk.Scrollbar(chat_frame)

msg_queue = tk.Listbox(chat_frame, height = 20, width = 60, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
msg_queue.pack(side = tk.LEFT, fill = tk.BOTH)
msg_queue.pack()

chat_frame.pack()

chat_field = tk.Entry(top, textvariable = my_msg)
chat_field.bind("<Return>", send)
chat_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", gui_close)


if __name__ == '__main__':
    RECEIVE_THREAD = Thread(target = receive)
    RECEIVE_THREAD.start()
    tk.mainloop()
