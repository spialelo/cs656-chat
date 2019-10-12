#!/usr/bin/env python3
"""This server is for multithreaded (asynchronous) chat application."""

from socket import AF_INET, socket, SOCK_STREAM
# SOCK_STREAM is a TCP connection
#TODOPWRPT: AF_INET - explain what it is
from threading import Thread

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave Now type your name and" +
        " press enter!","utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        #TODOPWRPT: what is Thread? why am I using it?

def handle_client(client):
    """Handles a single client connection."""
    name = client.recv(BUFFSIZE).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFSIZE)
        if msg != 

clients = {}
addresses = {}

HOST = ''
PORT = 3300
BUFFSIZE = 1024
ADDRESS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

