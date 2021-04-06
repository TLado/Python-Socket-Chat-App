import threading
import socket
import json

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()
users = []

class User():
    def __init__(self, name, ip, id_num):
        self.name = name
        self.ip = ip
        self.id = id_num
        self.status = 1
        self.log = []
        self.update()

    def update(self):
        with open("users.json", "r+") as json_file: # adding user to users.json
            data = json.load(json_file)
            user_info = {
                'name': self.name,
                'ip': self.ip,
                'id': self.id,
                'status': self.status,
                'log': self.log
            }
            app = True
            for i, obj in enumerate(data):
                if obj["name"] == self.name: # if it has already been created
                    if len(self.log) != 0 and self.status == 1:
                        user_info["log"] = obj["log"] + [self.log] # adding the previous messages to userinfo
                    else:
                        user_info["log"] = obj["log"] # if there is no new message
                    data[i] = user_info
                    app = False # making sure that we don't add a user twice
            if app:
                data.append(user_info)
            json_file.seek(0)
            json.dump(data, json_file)

    def update_log(self, message): # adds message to log 
        self.log = message
        self.update()
    
    def update_status(self): # updated status
        self.status = 0 if self.status == 1 else 1
        self.update()

    def print_values(self): # just for testing
        print(self.name, self.ip, self.id, self.status, self.log)


def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode(FORMAT) #the first "message" is the name
        if name == "@": # if the user didn't give a name, the name will be the id
            name = "@User" + addr[1]
        user = User(name, addr[0], addr[1]) # creating User object
        print(f"User {name} joined the chat")
        while True:
            msg = conn.recv(1024).decode(FORMAT) #getting the first 1024 bytes of the message

            if not msg: #if we did not receive content
                break

            if msg == DISCONNECT_MESSAGE: #if the user wants to disconnect
                user.update_status() # setting status to offline
                print(f"User {name} left the chat")
                break
            else:
                user.update_log(msg) # we add the message to the log
                print(f"[{name}] {msg}")
            
    finally:  # this will run every time, even if an error is in "try"
        with clients_lock:
            clients.remove(conn)
        conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock: # so that the object is modified one by one to avoid errors
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr)) 
        thread.start() # starting a thread


if __name__ == "__main__":
    start()
