"""Server for multithreaded (asynchronous) chat application."""
import socket
import threading
import sys

clients = {}
addresses = {}

IP = "127.0.0.1"
PORT = 33002
BUFFSIZE = 1024
ADDR = (IP, PORT)

""" Address Family - internet, SOCK_STREAM is the TCP connection; reliable """
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" reuse socket address to allow reconnecting """
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(ADDR)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = server_socket.accept()
        print("%s:%s has connected." % client_address)
        client.send(
            bytes("Welcome! Please type your username and press enter, to enter the chat!", "utf8"))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFFSIZE).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+"> ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            if len(clients) == 0:
                server_socket.close()
                sys.exit(0)
                break
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    """ Maximum 5 users is allowed """
    server_socket.listen(5)
    print("Waiting for connection...")
    accept_thread = threading.Thread(target=accept_incoming_connections)
    accept_thread.start()
    accept_thread.join()
    server_socket.close()
