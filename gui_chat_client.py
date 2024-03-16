
import tkinter as tk
import socket
import threading
import json
import re


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# window
window = tk.Tk()
window.title("Chat Client")
window.iconbitmap("icon.ico")
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
white = "#ffffff"
red = "#ff3855"
orange = "#ffaa1d"
yellow = "#fff700"
green = "#1fc742"
blue = "#5dadec"
purple = "#9c51b6"
window.config(bg=black)


class Connection:
    def __init__(self):
        self.encoder ="utf-8"
        self.bytesize = 1024
        self.port = 12345
        self.closing = False
        self.connecting = False
        self.receive_thread = None


# functions
def connect(connection):
    connection.connecting = True
    set_info("Connecting to the server...")
    # clear previous chats
    clear_chatbox()
    # collect info
    name = name_entry.get()
    target_ip = ip_entry.get()
    port = connection.port
    user_color = color.get()
    if not name or not target_ip or not port or not user_color:
        set_info("Check name, IP address, port and color.")
        return
    else:
        connection.name = name
        connection.target_ip = target_ip
        connection.port = port
        connection.color = user_color
    # verify ip address. it must be v4
    if not ip_verified(target_ip):
        set_info("Enter a valid IPv4 address.")
        return
    # verify port number, it must be integer
    try:
        connection.port = int(connection.port)
    except ValueError:
        set_info("Port value must be integer.")
        return
    # try to connect
    try:
        connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.client_socket.connect((connection.target_ip, int(connection.port)))
        message_json = connection.client_socket.recv(connection.bytesize)
        process_message(connection, message_json)
        set_info("Connected.")
        # enable gui for chat
        gui_start()
        connection.receive_thread = threading.Thread(target=receive_message, args=(connection, ))
        connection.receive_thread.start()
    except:
        set_info("Connection not established. Check host IP.")
    finally:
        connection.connecting = False


def disconnect(connection):
    """Disconnect the client from the server"""
    set_info("Ready.")
    connection.closing = True
    # create a message packet to be sent
    message_packet = create_message("DISCONNECT", connection.name, "I am leaving.", connection.color)
    connection.client_socket.send(message_packet.encode(connection.encoder))


    # Stop the receive thread if it exists
    # if connection.receive_thread:
    #     connection.receive_thread.join()
    #     connection.receive_thread = None
    # disable gui for chat
    gui_end()
    connection.closing = False

def gui_start():
    """Officially start connection by updating gui"""
    connect_button.config(state=tk.DISABLED)
    disconnect_button.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)
    input_entry.config(state=tk.NORMAL)
    name_entry.config(state=tk.DISABLED)
    ip_entry.config(state=tk.DISABLED)

    for button in color_buttons:
        button.config(state=tk.DISABLED)


def gui_end():
    """Officially end connection by updating gui"""
    connect_button.config(state=tk.NORMAL)
    disconnect_button.config(state=tk.DISABLED)
    send_button.config(state=tk.DISABLED)
    input_entry.config(state=tk.DISABLED)
    name_entry.config(state=tk.NORMAL)
    ip_entry.config(state=tk.NORMAL)

    for button in color_buttons:
        button.config(state=tk.NORMAL)


def create_message(flag, name, message, color):
    """Return a message packet"""
    message_packet = {
        'flag': flag,
        'name': name,
        'message': message,
        'color': color
    }
    message_json = json.dumps(message_packet)
    return message_json


def process_message(connection, message_json):
    # update chat history by first unpacking json message
    message_packet = json.loads(message_json)
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]
    if flag == "INFO":
        message_packet = create_message("INFO", connection.name, "Joins the server!", connection.color)
        connection.client_socket.send(message_packet.encode(connection.encoder))
    elif flag == "MESSAGE":
        # server has sent a message to display
        insert_text_to_chatbox(f"{name}: {message}\n", color)
    elif flag == "DISCONNECT":
        # server is asking you to leave.
        insert_text_to_chatbox(f"{name}: {message}\n", color)
        disconnect(connection)
    else:
        set_info("Error processing message.")


def send_message(connection):
    # send the message to the server
    message_packet = create_message("MESSAGE", connection.name, input_entry.get(), connection.color)
    connection.client_socket.send(message_packet.encode(connection.encoder))
    # clear entry
    input_entry.delete(0, tk.END)


def receive_message(connection):
    """Receive a message from the server"""
    while not connection.closing:
        try:
            connection.client_socket.settimeout(1)
            message_json = connection.client_socket.recv(connection.bytesize)
            if not message_json:  # If no data received, break the loop
                break
            process_message(connection, message_json)
        except ConnectionResetError:
            # Handle connection reset error (client disconnected by the server)
            if connection.closing:
                break
        except socket.timeout:
            if connection.closing:
                break
        except Exception as e:
            set_info("Error receiving message.")
            break


def ip_verified(ip):
    """Regular expression to match IPv4 address"""
    ip_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
    # Check if the entered string matches the IP address format
    if re.match(ip_regex, ip):
        return True
    else:
        return False


def clear_chatbox():
    chat_textbox.config(state=tk.NORMAL)
    chat_textbox.delete(1.0, tk.END)
    chat_textbox.config(state=tk.DISABLED)


def insert_text_to_chatbox(text, color):
    chat_textbox.config(state=tk.NORMAL)
    chat_textbox.insert(tk.END, text, color)
    chat_textbox.tag_configure(color, foreground=color)
    chat_textbox.config(state=tk.DISABLED)
    chat_textbox.yview(tk.END)


def message_enter_on_press(event):
    send_message(my_connection)


def set_info(text):
    info_label.config(text=text)
    
    
def on_closing():
    try:
        disconnect(my_connection)
    except:
        print("User closed the app.")
    finally:
        window.destroy()


"""GUI LAYOUT"""
# Frames
info_frame = tk.Frame(window, bg=black)
color_frame = tk.Frame(window, bg=black)
connection_frame = tk.Frame(window, bg=black)
output_frame = tk.Frame(window, bg=black)
input_frame = tk.Frame(window, bg=black)
info_frame.pack()
color_frame.pack()
connection_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# info frame layout
ip_label = tk.Label(info_frame, text="Host IP :", font=my_font, fg=orange, bg=black)
ip_entry = tk.Entry(info_frame, borderwidth=2, width=15, font=my_font)
name_label = tk.Label(info_frame, text="Your name :", font=my_font, fg=orange, bg=black)
name_entry = tk.Entry(info_frame, borderwidth=2, width=15, font=my_font)

ip_label.grid(row=0, column=0, padx=2, pady=5)
ip_entry.grid(row=0, column=1, padx=2, pady=5)
name_label.grid(row=0, column=2, padx=2, pady=10)
name_entry.grid(row=0, column=3, padx=2, pady=10)

# color frame layout
color = tk.StringVar()
color.set(white)
white_button = tk.Radiobutton(color_frame, width=0, text="White", variable=color, value=white, bg=black, fg=orange, font=my_font)
red_button = tk.Radiobutton(color_frame, width=0, text="Red", variable=color, value=red, bg=black, fg=orange, font=my_font)
orange_button = tk.Radiobutton(color_frame, width=5, text="Orange", variable=color, value=orange, bg=black, fg=orange, font=my_font)
yellow_button = tk.Radiobutton(color_frame, width=5, text="Yellow", variable=color, value=yellow, bg=black, fg=orange, font=my_font)
green_button = tk.Radiobutton(color_frame, width=5, text="Green", variable=color, value=green, bg=black, fg=orange, font=my_font)
blue_button = tk.Radiobutton(color_frame, width=5, text="Blue", variable=color, value=blue, bg=black, fg=orange, font=my_font)
purple_button = tk.Radiobutton(color_frame, width=5, text="Purple", variable=color, value=purple, bg=black, fg=orange, font=my_font)
color_buttons = [white_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

white_button.grid(row=1, column=0, padx=0, pady=0)
red_button.grid(row=1, column=1, padx=0, pady=0)
orange_button.grid(row=1, column=2, padx=2, pady=2)
yellow_button.grid(row=1, column=3, padx=2, pady=2)
green_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
purple_button.grid(row=1, column=6, padx=2, pady=2)

# connection frame layout
connect_button = tk.Button(connection_frame, text="Connect", font=my_font, bg=orange, borderwidth=5, width=10, command=lambda: connect(my_connection)) #
disconnect_button = tk.Button(connection_frame, text="Disconnect", font=my_font, bg=orange, borderwidth=5, width=10, state=tk.DISABLED, command=lambda: disconnect(my_connection))

connect_button.grid(row=0, column=2, padx=4, pady=5)
disconnect_button.grid(row=0, column=3, padx=4, pady=5)

# output frame layout
my_scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL)
chat_textbox = tk.Text(output_frame, height=20, width=55, borderwidth=3, bg=black, fg=orange, font=my_font, yscrollcommand=my_scrollbar.set, wrap=tk.WORD)
my_scrollbar.config(command=chat_textbox.yview)
chat_textbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# input frame layout
input_entry = tk.Entry(input_frame, width=45, borderwidth=3, font=my_font)
input_entry.bind("<Return>", message_enter_on_press)
send_button = tk.Button(input_frame, text="Send", borderwidth=5, width=10, font=my_font, bg=orange, state=tk.DISABLED, command=lambda: send_message(my_connection))
info_label = tk.Label(input_frame, text="Ready.", font=my_font, fg=orange, bg=black)

input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)
info_label.grid(row=1, column=0, sticky="W")

# connection state
my_connection = Connection()

# Define the function to be executed when the window is closed
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
