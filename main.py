import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def sendingMessage(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        # c.send(message.encode())
        print("You: " + message)


def receivingMessages(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())
        # print("Partner: " + c.recv(1024).decode())


threading.Thread(target=sendingMessage, args=(client,)).start()
threading.Thread(target=receivingMessages, args=(client,)).start()
