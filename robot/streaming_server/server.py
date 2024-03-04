# This is server code to send video frames over UDP
import cv2
import imutils
import socket
import base64
import logging
from threading import Thread
from typing import Tuple

logging.basicConfig(level=logging.INFO)

Address = Tuple[str, int]

BUFF_SIZE = 65536
FRAME_WIDTH = 600
TIMEOUT = 5


class ClientThread(Thread):
    def __init__(self, address: Address, server: socket.socket, vid: cv2.VideoCapture) -> None:
        super().__init__()
        self.address = address
        self.server = server
        self.vid = vid
        self.stop = False

    def run(self):
        while self.vid.isOpened() and not self.stop:
            _, frame = self.vid.read()
            frame = imutils.resize(frame, width=FRAME_WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)

            try:
                self.server.sendto(message, self.address)
            except Exception as exc:
                logging.error(str(exc))

        logging.info(f"Closing connection with: {self.address}")


def _create_socket(address: Address) -> socket.socket:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    server.bind(address)

    return server


def _connect_client(server: socket.socket) -> Address:
    _, client_address = server.recvfrom(1024)
    server.sendto(
        str.encode("Connected"),
        client_address
    )
    logging.info(f"Connection from: {client_address}")

    return client_address


def main(host: str, port: int) -> None:
    address = (host, port)

    vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
    server = _create_socket(address)
    logging.info(f'Waiting for connections on {address}')

    prev_conn = None
    while True:
        client_address = _connect_client(server)
        if prev_conn:
            prev_conn.stop = True

        thread = ClientThread(client_address, server, vid)
        thread.start()
        prev_conn = thread


main(host='10.0.0.9', port=1234)
