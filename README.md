# Python-Socket-Chat-App

This is a **chat app** made with python using sockets.

The users are able to connect to the server (in this case "localhost") and send messages. 

The first message is always the *name* of the user, the actual messages are then printed out by [server.py](https://github.com/TLado/python-socket-chat-app/blob/main/server.py).

The user can quit anytime just by typing "*q*". 

All of the users data is logged in a json file ([users.json](https://github.com/TLado/python-socket-chat-app/blob/main/users.json)), including: 
- username
- ip-address
- unique id
- status
- messages

> users with the **same name** are treated as the same user, so if the user logs out and than back in, the messages are saved to the same list.