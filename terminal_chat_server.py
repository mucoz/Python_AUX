
import socket
import threading

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 1234
ENCODER = "utf-8"
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.close()
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

client_socket_list = []
client_name_list = []


def broadcast_message(message):
    for client_socket in client_socket_list:
        client_socket.send(message)


def receive_message(client_socket):
    while True:
        try:
            # get index of the client_socket in client_socket_list
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            message = f"{name} : {message}".encode(ENCODER)
            broadcast_message(message)
        except:
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]
            client_socket_list.remove(client_socket)
            client_name_list.remove(name)
            client_socket.close()
            broadcast_message(f"{name} has left the chat!".encode(ENCODER))
            break


def connect_client():
    while True:
        # Accept any incoming client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected with {client_address}...")
        client_socket.send("NAME".encode(ENCODER))
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER).capitalize()
        client_socket_list.append(client_socket)
        client_name_list.append(client_name)
        print(f"Name of new client is {client_name}\n")
        client_socket.send(f"{client_name}, you have connected to the server!".encode(ENCODER))
        broadcast_message(f"{client_name} has joined the chat".encode(ENCODER))

        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()


print(f"Server is listening for incoming connections...\n")
connect_client()
