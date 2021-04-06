import socket
import time
import re

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect(): #create connection object between server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(ADDR)
    return client


def send(client, msg): # sends message to server
    message = msg.encode(FORMAT)
    client.send(message)


def start():
    answer = input('Would you like to connect (y/n)? ')
    if answer.lower() != 'y':
        return

    connection = connect()
    name = "@" + input("Enter your name: ")
    send(connection, name) # sending the name to the server
    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q': 
            break

        if re.match("^\s+$", msg): # not letting the user send only whitespaces
            continue

        send(connection, msg) # sending the message to the server

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(0.01) # we need this because of threading
    print('Disconnected')


if __name__ == "__main__":
    start()
