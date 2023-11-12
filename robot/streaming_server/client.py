# This is client code to receive video frames over UDP
import cv2
import socket
import numpy as np
import time
import base64
import logging

logging.basicConfig(level=logging.INFO)

Address = tuple[str, int]

BUFF_SIZE = 65536
TIMEOUT = 10


def _create_client() -> socket.socket:
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
	client.settimeout(TIMEOUT)
	return client


def _connect_to_server(client: socket.socket, server_address: Address) -> str:
	client.sendto(
		str.encode("ping"),
		server_address
	)

	message, _ = client.recvfrom(1024)
	return message.decode()


def _receive_data(client: socket.socket, server_address: Address) -> None:
	fps, st, frames_to_count, cnt = (0, 0, 20, 0)

	while True:
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			client.sendto(str.encode("COMMAND: STOP"), server_address)
			break

		client.sendto(str.encode("ping"), server_address)
		packet, _ = client.recvfrom(BUFF_SIZE)
		logging.info(f"Received packet size: {len(packet)}")

		data = base64.b64decode(packet, ' /')
		npdata = np.fromstring(data, dtype=np.uint8)
		frame = cv2.imdecode(npdata, 1)
		frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.imshow("RECEIVING VIDEO", frame)

		if cnt == frames_to_count:
			fps = round(frames_to_count / (time.time() - st))
			st = time.time()
			cnt = 0

		cnt += 1


def main(host: str, port: int) -> None:
	server_address = (host, port)

	client = _create_client()

	msg = _connect_to_server(client, server_address)

	if msg != "Connected":
		logging.info(f"Couldn't connect to server, reason: {msg}")
		return
	logging.info(f"Connected to server: {server_address}")

	_receive_data(client, server_address)
	logging.info(f"Disconnected from server: {server_address}")


if __name__ == "__main__":
	main(host='51.83.134.183', port=9000)
