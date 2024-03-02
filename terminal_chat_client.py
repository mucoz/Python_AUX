
import socket
import threading

DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 1234
ENCODER = "utf-8"
BYTESIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))


def send_message():
    while True:
        message = input("")
        client_socket.send(message.encode(ENCODER))


def receive_message():
    while True:
        try:
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            if message == "NAME":
                name = input("What is your name : ")
                client_socket.send(name.encode(ENCODER))
            else:
                print(message)
        except:
            print("An error occured...")
            client_socket.close()
            break


receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

receive_thread.start()
send_thread.start()
