import socket
import threading

import rsa

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()
    client, _ = server.accept()
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))
else:
    exit()


def sendingMessage(c):
    while True:
        message = input("")
        c.send(message.encode())
        print("You: " + message)


def receivingMessages(c):
    while True:
        print("Partner: " + c.recv(1024).decode())


threading.Thread(target=sendingMessage, args=(client,)).start()
threading.Thread(target=receivingMessages, args=(client,)).start()
