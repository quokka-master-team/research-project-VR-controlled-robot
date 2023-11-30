import socket

server_ip = '10.0.0.9'
server_port = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    command = input("Enter command to send to server: ")
    client_socket.send(command.encode())
