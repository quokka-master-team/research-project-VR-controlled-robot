import av
from typing import Any, Self
from src.stream.domain.dtos import StreamUnitDto
import socket
from src.config import Settings


class Transmission:
    def __init__(self, unit: StreamUnitDto, settings: Settings) -> None:
        self._unit = unit
        self._stream_pipeline = settings.STREAM_PIPELINE
        self._stream_destination_ip = settings.STREAM_DESTINATION_IP
        self._stream_destination_port = settings.STREAM_DESTINATION_PORT

    def _create_client(self) -> socket.socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self._unit.host, self._unit.port))

        return client

    @staticmethod
    def _send_commands(client: socket.socket, commands: list[str]) -> None:
        for command in commands:
            print(f"Sending command: {command}", flush=True)
            client.send(command.encode() + b"\n")
            print(f"Receiving {client.recv(1024)}")

    def _setup(self) -> None:
        client = self._create_client()
        self._send_commands(
            client,
            commands=[
                "STOP",
                f"RTSP {self._stream_destination_ip} {self._stream_destination_port}",
                f"USE {self._stream_pipeline}",
                "START",
                "DISCONNECT",
            ],
        )
        client.close()

    def _stop_transmission(self) -> None:
        client = self._create_client()
        self._send_commands(client, commands=["STOP", "DISCONNECT"])
        client.close()

    def __enter__(self) -> Self:
        self._setup()
        self.av_container = av.open(
            f"rtsp://{self._stream_destination_ip}:{self._stream_destination_port}/stream",
        )
        # self._content = self.av_container.decode(video=0)
        return self

    def __exit__(self, *args: Any) -> None:
        self.av_container.close()
        self._stop_transmission()

    # def receive_data(self) -> bytes:
    #     return next(self._content)
