import socket
import sys

HOST, PORT = sys.argv[1], int(sys.argv[2])
print(HOST)
print(PORT)
#HOST, PORT = "127.0.0.1", 8888
#HOST, PORT = "140.112.42.108", 7777
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
while(True):
    response = input(client.recv(1000).decode("utf-8"))
    response = str(response)
    client.send(response.encode())
