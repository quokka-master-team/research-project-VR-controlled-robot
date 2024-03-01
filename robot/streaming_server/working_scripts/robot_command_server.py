import asyncio
import websockets
from talker import RobotController

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
        #await self.create_robot_controller()

    async def start(self):
        print(f"Server listening on {self.ip}:{self.port}")
        await self.create_robot_controller()
        async with websockets.serve(self.handle_client, self.ip, self.port):
            await asyncio.Future()

    async def handle_client(self, websocket, path):
        print(f"Connection request from {websocket.remote_address}")

        try:
            async for data in websocket:
                print(f"Received from {websocket.remote_address}: {data}")
                await self.process_command(data, websocket.remote_address)

        except websockets.ConnectionClosedOK:
            pass

        print(f"Connection with {websocket.remote_address} closed.")

    async def create_robot_controller(self):
        self.robot_controller = RobotController()
        self.robot_controller.init_node()

    async def process_command(self, command, client_address):
        command_method_name = self.command_handlers.get(command.lower())
        if command_method_name:
            command_method = getattr(self, command_method_name, None)
            if command_method:
                await command_method(client_address)
            else:
                print(f"Command handler not found for {command}")
        else:
            print(f"Unknown command received from {client_address}: {command}")

    async def forward_command(self, client_address):
        print(f"Received command FORWARD from {client_address}")
        self.robot_controller.move_forward()

    async def left_command(self, client_address):
        print(f"Received command LEFT from {client_address}")
        self.robot_controller.move_left()

    async def right_command(self, client_address):
        print(f"Received command RIGHT from {client_address}")
        self.robot_controller.move_right()

    async def backward_command(self, client_address):
        print(f"Received command BACKWARD from {client_address}")
        self.robot_controller.move_backward()

    async def stop_command(self, client_address):
        print(f"Received command STOP from {client_address}")
        self.robot_controller.stop()

    async def arm_command(self, client_address):
        print(f"Received command ARM from {client_address}")
        self.robot_controller.arm_pixhawk()

    async def disarm_command(self, client_address):
        print(f"Received command DISARM from {client_address}")
        self.robot_controller.disarm_pixhawk()

if __name__ == "__main__":
    server_instance = Server(ip='10.0.0.9', port=5001)
    asyncio.run(server_instance.start())
