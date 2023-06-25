import cv2
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-url', '--url', help='URL of image to capture', required=True)

raspberry_url = vars(parser.parse_args()).get('url')
capture = cv2.VideoCapture(raspberry_url)

while True:
    success, frame = capture.read()

    cv2.imshow('asd', frame)
    cv2.waitKey(1)