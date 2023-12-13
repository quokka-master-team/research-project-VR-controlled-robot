#!/usr/bin/env python3
# Software License Agreement (BSD License)

import socket
from talker2 import RobotController

class Server:
    command_handlers = {
        'forward': 'forward_command',
        'left': 'left_command',
        'right': 'right_command',
        'backward': 'backward_command',
        'stop': 'stop_command',
        'arm': 'arm_command',
        'disarm': 'disarm_command',
    }

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)  # Allow only one connection
        self.create_robot_controller()

    def start(self):
        print(f"Server listening on {self.ip}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection request from {client_address}")
                #print("Disarming Pixhawk...")
                #self.robot_controller.disarm_pixhawk()

                try:
                    while True:
                        data = client_socket.recv(1024).decode()
                        if not data:
                            break
                        print(f"Received from {client_address}: {data}")
                        self.process_command(data, client_address)

                except KeyboardInterrupt:
                        print("Server shutting down...")
                        self.server_socket.close()
                        print("Server shutdown complete.")

                print(f"Connection with {client_address} closed.")
                client_socket.close()
                print("Disarming Pixhawk...")
                self.robot_controller.disarm_pixhawk()

        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_socket.close()
            print("Server shutdown complete.")

    def create_robot_controller(self):
        self.robot_controller = RobotController()
        self.robot_controller.init_node()

    def process_command(self, command, client_address):
        command_method_name = self.command_handlers.get(command.lower())
        if command_method_name:
            command_method = getattr(self, command_method_name, None)
            if command_method:
                command_method(client_address)
            else:
                print(f"Command handler not found for {command}")
        else:
            print(f"Unknown command received from {client_address}: {command}")

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

    def arm_command(self, client_address):
        print(f"Received command ARM from {client_address}")
        self.robot_controller.arm_pixhawk()

    def disarm_command(self, client_address):
        print(f"Received command DISARM from {client_address}")
        self.robot_controller.disarm_pixhawk()

if __name__ == "__main__":
    server_instance = Server(ip='10.0.0.9', port=5001)
    server_instance.start()
