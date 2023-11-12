# This is server code to send video frames over UDP
import cv2
import imutils
import socket
import base64
import logging

logging.basicConfig(level=logging.INFO)

Address = tuple[str, int]

BUFF_SIZE = 65536
FRAME_WIDTH = 600
TIMEOUT = 5


def _create_socket(address: Address) -> socket.socket:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    server.bind(address)

    return server


def _connect_client(server: socket.socket) -> Address:
    server.settimeout(None)

    _, client_address = server.recvfrom(1024)
    server.sendto(
        str.encode("Connected"),
        client_address
    )
    logging.info(f"Connection from: {client_address}")

    return client_address


def _send_data(server: socket.socket, client_address: Address, vid: cv2.VideoCapture) -> None:
    server.settimeout(TIMEOUT)

    while vid.isOpened():
        try:
            message, address = server.recvfrom(1024)
        except TimeoutError:
            break

        if address != client_address:
            server.sendto(
                str.encode("Cannot connect to server, other client is connected"),
                address
            )
            continue

        if message.decode() == "COMMAND: STOP":
            break

        _, frame = vid.read()
        frame = imutils.resize(frame, width=FRAME_WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        server.sendto(message, client_address)


def main(host: str, port: int) -> None:
    address = (host, port)

    vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
    server = _create_socket(address)
    logging.info(f'Waiting for connections on {address}')

    while True:
        client_address = _connect_client(server)
        _send_data(server, client_address, vid)
        logging.info(f"Closing connection with: {client_address}")


if __name__ == "__main__":
    main(host='10.0.0.9', port=1234)
