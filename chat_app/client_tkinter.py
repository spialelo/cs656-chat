"""Tkinter GUI chat client."""
import socket
import threading
import tkinter as tk

firstclick = True
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#----Socket code----
# IP = input('Enter host IP: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33002
# else:
#     PORT = int(PORT)

IP = "127.0.0.1"
PORT = 33002

BUFFSIZE = 1024
ADDR = (IP, PORT)

MSG_COUNT = 0

""" Address Family - internet, SOCK_STREAM is the TCP connection; reliable """
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" reuse socket address to allow reconnecting """
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)



def on_entry_click(event):
    """function that gets called whenever entry1 is clicked"""
    global firstclick

    if firstclick:  # if this is the first time they clicked it
        firstclick = False
        entry_field.delete(0, "end")  # delete all the text in the entry


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            msg_list.insert(tk.END, msg)
            
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global MSG_COUNT
    msg = my_msg.get()

    """" Update chat window with current user's name/username """
    if MSG_COUNT == 0 and msg != "{quit}":
        window.title(msg)

    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    MSG_COUNT += 1

    if msg == "{quit}":
        client_socket.close()
        window.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


window = tk.Tk()
window.title("Chat Room")
window.geometry("400x350")

messages_frame = tk.Frame(window)
my_msg = tk.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tk.Listbox(messages_frame, height=15, width=50,
                   yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(window, textvariable=my_msg)

entry_field.bind('<FocusIn>', on_entry_click)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(window, text="Send", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = threading.Thread(target=receive)
receive_thread.start()
window.mainloop()
