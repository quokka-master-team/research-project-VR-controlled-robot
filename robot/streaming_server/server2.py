#!/usr/bin/env python3
# Software License Agreement (BSD License)

import socket
import threading
import multiprocessing
from talker2 import RobotController

class Server:
    # Dictionary mapping commands to functions
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
        self.server_socket.listen(5)
        self.client_handlers = {}
        self.robot_controller = None
        print(threading.current_thread())
        print(threading.main_thread())

    def start(self):
        print(f"Server listening on {self.ip}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection request from {client_address}")

                # Create a new thread to handle the client
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
                self.create_robot_controller()
                self.client_handlers[client_address] = client_handler
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_socket.close()
            for client_handler in self.client_handlers.values():
                client_handler.join()
            print("Server shutdown complete.")

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
        print("Terminate ROS")
        self.robot_controller.terminate_ros_process()

    def create_robot_controller(self):
        self.robot_controller = RobotController()
        self.robot_controller.init_node()

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
        print(f"Robot armed - received command from {client_address}")
        self.robot_controller.arm_pixhawk()

    def disarm_command(self, client_address):
        print(f"Robot disarmed - received command from {client_address}")
        self.robot_controller.disarm_pixhawk()

if __name__ == "__main__":
    # Create an instance of the Server class with the desired IP and port
    server_instance = Server(ip='10.0.0.9', port=5001)

    # Start the server
    server_instance.start()