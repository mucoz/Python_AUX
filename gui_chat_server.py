import sys
import tkinter as tk
from tkinter import messagebox as msg
import socket
import threading
import json


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600



window = tk.Tk()
window.title("Chat Server")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (WINDOW_WIDTH / 2))
y_cordinate = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
window.resizable(True, True)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

# fonts and colors
my_font = ('SimSun', 14)
black = "#010101"
orange = "#fb7e14"
window.config(bg=black)


# Connection class to store server socket info
class Connection:

    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 12345
        self.encoder = "utf-8"
        self.bytesize = 1024
        self.closing = False
        self.connect_thread = None
        self.receive_thread = None
        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []


def start_server(connection):
    # create server socket
    connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.server_socket.bind((connection.host_ip, connection.port))
    connection.server_socket.listen()

    # update gui
    clear_chatbox()
    insert_text_to_chatbox(f"Server started on IP {connection.host_ip} port {connection.port}.", orange)
    end_button.config(state=tk.NORMAL)
    self_broadcast_button.config(state=tk.NORMAL)
    message_button.config(state=tk.NORMAL)
    kick_button.config(state=tk.NORMAL)
    ban_button.config(state=tk.NORMAL)
    start_button.config(state=tk.DISABLED)
    # create a thread to listen to clients
    connection.connect_thread = threading.Thread(target=connect_client, args=(connection, ))
    connection.connect_thread.start()


def end_server(connection):
    connection.closing = True
    # alert all users of ending the server
    message_packet = create_message("DISCONNECT", "Admin (broadcast)", "Server is closing...", orange)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))
    # update gui
    insert_text_to_chatbox(f"Server closing on port {connection.port}.", orange)
    end_button.config(state=tk.DISABLED)
    self_broadcast_button.config(state=tk.DISABLED)
    message_button.config(state=tk.DISABLED)
    kick_button.config(state=tk.DISABLED)
    ban_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)

    # close server socket
    connection.server_socket.close()
    connection.closing = False


def connect_client(connection):
    """Connect an incoming client to the server"""
    while not connection.closing:
        try:
            # set a timeout on the server socket
            connection.server_socket.settimeout(1)  # 1 second timeout
            client_socket, client_address = connection.server_socket.accept()
            if client_address[0] in connection.banned_ips:
                message_packet = create_message("DISCONNECT", "Admin (private)", "You have been banned.", orange)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))
                client_socket.close()
            else:
                message_packet = create_message("INFO", "Admin (private)", "Please send your name", orange)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))
                # wait for confirmation
                message_json = client_socket.recv(connection.bytesize)
                process_message(connection, message_json, client_socket, client_address)
        except ConnectionResetError:  # Catch the exception when the client closes the connection abruptly            if connection.closing:
            if connection.closing:
                break
        except socket.timeout:
            if connection.closing:
                break
        except Exception as e:
            if connection.closing:
                break
    sys.exit()


def create_message(flag, name, message, color):
    """Return a message packet to be sent"""
    message_packet = {
        'flag': flag,
        'name': name,
        'message': message,
        'color': color
    }
    return message_packet


def process_message(connection, message_json, client_socket, client_address=(0,0)):
    """Update server info"""
    message_packet = json.loads(message_json)
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]
    if flag == "INFO":
        # add the new client info to the lists
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])
        # broadcast the new client joining
        message = f"{name} has joined the server."
        message_packet = create_message("MESSAGE", "Admin (broadcast)", message, orange)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))
        insert_text_to_chatbox(message, orange)
        # update server UI
        client_listbox.insert(tk.END, f"Name :{name}         IP Addr : {client_address[0]}")
        # start a thread to receive messages
        connection.receive_thread = threading.Thread(target=receive_message, args=(connection, client_socket, ))
        connection.receive_thread.start()
    elif flag == "MESSAGE":
        broadcast_message(connection, message_json)
        insert_text_to_chatbox(f"{name}: {message}", color)

    elif flag == "DISCONNECT":
        # close/remove client
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()

        # alert all users that the client has left the chat
        message_packet = create_message("MESSAGE", "Admin (broadcast)", f"{name} has left the chat.")
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # update the server ui
        insert_text_to_chatbox(f"Admin (broadcast): {name} has left the chat.", orange)
    else:
        # catch for errors
        insert_text_to_chatbox("Error processing message...", orange)


def broadcast_message(connection, message_json):
    """Send a message to all client sockets connected to the server"""
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)


def receive_message(connection, client_socket):
    """Receive incoming message from a client"""
    while not connection.closing:
        try:
            connection.server_socket.settimeout(1)
            message_json = client_socket.recv(connection.bytesize)
            if not message_json:  # If no data received, break the loop
                break
            process_message(connection, message_json, client_socket)
        except ConnectionResetError:
            if connection.closing:
                break
        except socket.timeout:
            if connection.closing:
                break
        except:
            break
    # Close the client socket when the loop exits
    client_socket.close()


def self_broadcast(connection):
    """Broadcast a special admin message to all clients"""
    message = input_entry.get()
    message_packet = create_message("MESSAGE", "Admin (broadcast)", message, orange)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))
    #show the message on the list
    insert_text_to_chatbox(f"Admin (broadcast): {message}", orange)
    # chat_textbox.insert(0, f"Admin (broadcast): {message}")
    # clear input entry
    input_entry.delete(0, tk.END)


def private_message(connection):
    """Send a private message to a single client"""
    selection = client_listbox.curselection()
    if selection:
        index = selection[0]
        client_socket = connection.client_sockets[index]
        # create a message packet and send
        message_packet = create_message("MESSAGE", "Admin (private)", input_entry.get(), orange)
        message_json = json.dumps(message_packet)
        client_socket.send(message_json.encode(connection.encoder))

        # clear input entry
        input_entry.delete(0, tk.END)
    else:
        msg.showinfo("Warning", "You need to select a user from the list.")


def kick_client(connection):
    """Kick a client"""
    # select a client from the list
    selection = client_listbox.curselection()
    if selection:
        index = selection[0]
        client_socket = connection.client_sockets[index]
        # create the message packet
        message_packet = create_message("DISCONNECT", "Admin (private)", "You have been kicked.", orange)
        message_json = json.dumps(message_packet)
        client_socket.send(message_json.encode(connection.encoder))
    else:
        msg.showinfo("Warning", "You need to select a user from the list.")


def ban_client(connection):
    """Ban a client"""
    selection = client_listbox.curselection()
    if selection:
        index = selection[0]
        client_socket = connection.client_sockets[index]
        # create the message packet
        message_packet = create_message("DISCONNECT", "Admin (private)", "You have been banned.", orange)
        message_json = json.dumps(message_packet)
        client_socket.send(message_json.encode(connection.encoder))
        # ban the ip address of the client
        connection.banned_ips.append(connection.client_ips[index])
    else:
        msg.showinfo("Warning", "You need to select a user from the list.")


def copy_ip_to_clipboard(connection):
    window.clipboard_clear()
    window.clipboard_append(connection.host_ip)


def clear_chatbox():
    chat_textbox.config(state=tk.NORMAL)
    chat_textbox.delete(1.0, tk.END)
    chat_textbox.config(state=tk.DISABLED)


def insert_text_to_chatbox(text, color):
    chat_textbox.config(state=tk.NORMAL)
    chat_textbox.insert(tk.END, text + "\n", color)
    chat_textbox.tag_configure(color, foreground=color)
    chat_textbox.config(state=tk.DISABLED)
    chat_textbox.yview(tk.END)


def message_enter_on_press(event):
    self_broadcast(my_connection)


def on_closing():
    try:
        end_server(my_connection)
    except:
        print("User closed the app.")
    finally:
        window.destroy()


# GUI Layout
# frames
connection_frame = tk.Frame(window, bg=black)
history_frame = tk.Frame(window, bg=black)
client_frame = tk.Frame(window, bg=black)
message_frame = tk.Frame(window, bg=black)
admin_frame = tk.Frame(window, bg=black)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()

# connection frame layout
start_button = tk.Button(connection_frame, text="Start Server", borderwidth=5, width=15, font=my_font, bg=orange, command=lambda: start_server(my_connection) )
end_button = tk.Button(connection_frame, text="End Server", borderwidth=5, width=15, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: end_server(my_connection))

start_button.grid(row=0, column=2, padx=2, pady=10)
end_button.grid(row=0, column=3, padx=2, pady=10)

# history frame layout
history_scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL)
chat_textbox = tk.Text(history_frame, height=10, width=55, borderwidth=3, font=my_font, bg=black, fg=orange, yscrollcommand=history_scrollbar.set, wrap=tk.WORD)
history_scrollbar.config(command=chat_textbox.yview)

chat_textbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky="NS")

# client frame layout
client_scrollbar = tk.Scrollbar(client_frame, orient=tk.VERTICAL)
client_listbox = tk.Listbox(client_frame, height=10, width=55, borderwidth=3, font=my_font, bg=black, fg=orange, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=client_listbox.yview)

client_listbox.grid(row=0, column=0)
client_scrollbar.grid(row=0, column=1, sticky="NS")

# message frame layout
input_entry = tk.Entry(message_frame, width=40, borderwidth=3, font=my_font)
input_entry.bind("<Return>", message_enter_on_press)
self_broadcast_button = tk.Button(message_frame, text="Broadcast", width=13, borderwidth=5, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: self_broadcast(my_connection))

input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)

# admin frame layout
message_button = tk.Button(admin_frame, text="PM", borderwidth=5, width=11, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: private_message(my_connection))
kick_button = tk.Button(admin_frame, text="Kick", borderwidth=5, width=11, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: kick_client(my_connection))
ban_button = tk.Button(admin_frame, text="Ban", borderwidth=5, width=11, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: ban_client(my_connection))
copy_ip_button = tk.Button(admin_frame, text="Copy IP", borderwidth=5, width=11, font=my_font, bg=orange, state=tk.NORMAL, command=lambda: copy_ip_to_clipboard(my_connection))

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)
copy_ip_button.grid(row=0, column=3, padx=5, pady=5)

my_connection = Connection()


# Define the function to be executed when the window is closed
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
