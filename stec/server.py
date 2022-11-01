from ec_model import EmotionClassifier
from sm_model import Summarizer

import json
import socket
import threading
import time
import sys

HEADER = 64
FORMAT = 'utf-8'
PORT = 25566
IP = socket.gethostbyname(socket.gethostname())
DISCONNECT = '$$DISCONNECT'
CLOSE = '$$CLOSE'

print(f'Server starting on port {PORT} with IP ███.███.██.██')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
running = True

sm = Summarizer()
sm.load_model()

ec = EmotionClassifier()
ec.load_model()

def predict(text):
    summary = sm.predict(text)
    print(summary)

    data = ec.predict(summary)
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    print(data)

    return (summary, data)

def send(conn, msg):
    message = msg.encode(FORMAT)
    length = len(message)
    send_length = str(length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_requests(conn, addr):
    print(f'██.██.██.███ connected on port {PORT}.')
    connected = True

    while connected:
        length = conn.recv(HEADER).decode(FORMAT)
        
        if length:
            msg = conn.recv(int(length)).decode(FORMAT)
            print(f'██.██.██.███: {msg}')

            if msg == DISCONNECT:
                print(f'██.██.██.███ disconnected from port {PORT}.')
                connected = False
                return
            
            if msg == CLOSE:
                print(f'██.██.██.███ is closing the server.')
                running = False
                sys.exit()
                return

            try:
                prediction = predict(msg)
                send(conn, prediction[0])
                send(conn, json.dumps(prediction[1]))
            except:
                send(conn, '$$ERROR')
                send(conn, json.dumps(dict()))
    
    conn.close()

def start_server():
    server.listen()

    print(f'Server active on port {PORT} with IP ███.███.██.██')

    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_requests, args=(conn, addr))
        thread.start()
        print(f'{threading.activeCount() - 1} users are currently connected.')

start_server()
get_input = input('Server has been closed. Press any key to continue\n')

