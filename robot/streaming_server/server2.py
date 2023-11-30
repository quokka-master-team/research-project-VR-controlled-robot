import socket
import threading
from talker2 import RobotController

class Server:
    # Dictionary mapping commands to functions
    command_handlers = {
        'establish_connection': 'establish_connection_command',
        'forward': 'forward_command',
        'left': 'left_command',
        'right': 'right_command',
        'backward': 'backward_command',
        'stop': 'stop_command',
        'lose_connection': 'lose_connection_command',
    }

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.client_handlers = {}
        self.robot_controller = RobotController()

    def start(self):
        print(f"Server listening on {self.ip}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection request from {client_address}")

            # Create a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

            # Store the client handler in the dictionary
            self.client_handlers[client_address] = client_handler

    def handle_client(self, client_socket, client_address):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received from {client_address}: {data}")
            self.process_command(data, client_address)

        print(f"Connection with {client_address} closed.")
        del self.client_handlers[client_address]
        client_socket.close()

    def process_command(self, command, client_address):
        # Use the dictionary to get the corresponding function
        command_method_name = self.command_handlers.get(command.lower())
        if command_method_name:
            # Call the function with client_address as an argument
            command_method = getattr(self, command_method_name, None)
            if command_method:
                command_method(client_address)
            else:
                print(f"Command handler not found for {command}")
        else:
            print(f"Unknown command received from {client_address}: {command}")

    def establish_connection_command(self, client_address):
        print(f"Connection established with {client_address}")
        self.robot_controller.establish_connection()

    def forward_command(self, client_address):
        print(f"Received command FORWARD from {client_address}")
        self.robot_controller.move_forward()

    def left_command(self, client_address):
        print(f"Received command LEFT from {client_address}")
        self.robot_controller.move_left()

    def right_command(self, client_address):
        print(f"Received command RIGHT from {client_address}")
        self.robot_controller.move_right()

    def backward_command(self, client_address):
        print(f"Received command BACKWARD from {client_address}")
        self.robot_controller.move_backward()

    def stop_command(self, client_address):
        print(f"Received command STOP from {client_address}")
        self.robot_controller.stop()

    def lose_connection_command(self, client_address):
        print(f"Connection lost with {client_address}")
        self.robot_controller.lose_connection()

if __name__ == "__main__":
    # Create an instance of the Server class with desired IP and port
    server_instance = Server(ip='10.0.0.9', port=5001)

    # Start the server
    server_instance.start()
